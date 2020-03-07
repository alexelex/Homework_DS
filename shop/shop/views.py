# -*- coding: utf-8 -*-#
import json
import logging

from shop.decorators import access_and_errors
from shop.models import Products
from shop.exceptions import RequestFatal, RequestWarning

logger = logging.getLogger(__name__)


def parse_field(data, var, name, to_dict=False):
    if var is not None:
        if to_dict:
            try:
                var = json.loads(var)
            except ValueError:
                return
        data.update({name: var})


def parse_data(request, required_params=[], optional_params=[]):
    logger.debug("parse_data")
    data = {}
    if request.method == 'PUT':
        try:
            reader = request.body.decode()
            reader = reader.replace("\'", "\"")
            if not reader:
                raise RequestFatal(400, 'expected data in json format (current data is empty)')
            reader = json.loads(reader)
        except RequestFatal as e:
            raise e
        except Exception as e:
            raise RequestFatal(400, 'expected data in json format')

    for field in required_params + optional_params:
        if request.method == 'POST':
            parse_field(data, request.POST.get(field), field)
        elif request.method == 'PUT':
            parse_field(data, reader.get(field), field)
        elif request.method == 'GET':
            parse_field(data, request.GET.get(field), field)
        elif request.method == 'DELETE':
            parse_field(data, request.GET.get(field), field)

    for field in required_params:
        if field not in data:
            raise RequestFatal(
                400, 'required field: {}'.format(field))
    return data


def check_request_type(request, request_type):
    logger.debug("check_request_type")
    if request.method != request_type:
        raise RequestFatal(
            400, 'expected {} request'.format(request_type))


def add_product(data):
    note, created = Products.objects.get_or_create(
        code=data['code'],
    )

    if not created:
        raise RequestWarning(208)
    Products.objects.filter(code=data['code']).update(**data)


def delete_product(data):
    note = Products.objects.filter(
        code=data['code'],
    )

    if note.exists():
        note.delete()
    else:
        raise RequestFatal(404)


def update_product(code, data):
    note = Products.objects.filter(
        code=code,
    )

    if not note.exists():
        raise RequestFatal(404)
    if note.count() > 1:
        raise RequestFatal(500)
    note.update(**data)


def get_product_json(product):
    data = {
        'name': product.name,
        'code': product.code,
        'category': product.category,
        'create time': product.time_create,
        'modified time': product.time_modified,
    }

    if product.author:
        data.update({'author': product.author})
    if product.modifier:
        data.update({'modifier': product.modifier})
    return data


@access_and_errors
def product_create(request):
    logger.debug("product_create")
    check_request_type(request, 'POST')
    logger.info(request.POST)
    data = parse_data(
        request=request,
        required_params=['name', 'code', 'category'])
    # TODO: add author to data
    add_product(data)


@access_and_errors
def product_delete(request):
    logger.debug("product_delete")
    check_request_type(request, 'DELETE')
    data = parse_data(
        request=request,
        required_params=['code'])
    # TODO: add author to data as modifier
    delete_product(data)


@access_and_errors
def product_edit(request):
    logger.debug("product_edit")
    check_request_type(request, 'PUT')

    if 'code' not in request.GET:
        raise RequestFatal(400, 'required field: code')
    code = request.GET.get('code')

    data = parse_data(
        request=request,
        optional_params=['category', 'name'])
    # TODO: add author to data as modifier
    update_product(code, data)


@access_and_errors
def products_list(request):
    logger.debug("products_list")
    check_request_type(request, 'GET')
    list_num = int(request.GET.get('list', '0'))
    list_size = int(request.GET.get('size', '100'))

    products = Products.objects.all().order_by('time_create')
    products_count = products.count()
    if products_count < list_num * list_size:
        return {'products': []}

    products = products[list_size * list_num: list_size * (list_num + 1)]
    response = {'products': [get_product_json(product) for product in products]}

    if products_count > list_size * (list_num + 1):
        response.update({
            'next-url': 'database/products_list?list={}&&size={}'.format(list_num + 1, list_size)})
    return response


@access_and_errors
def product_info(request):
    logger.debug("product_info")
    check_request_type(request, 'GET')
    if 'code' not in request.GET:
        raise RequestFatal(400, 'required field: code')
    code = request.GET.get('code')

    products = Products.objects.filter(code=code)
    if len(products) > 1:
        raise RequestFatal(500, 'More than one product with code {}'.format(code))
    if len(products) == 0:
        raise RequestFatal(404)
    return get_product_json(products[0])
