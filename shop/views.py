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
    if request.method in ('PUT', 'POST'):
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
        if request.method in ('PUT', 'POST'):
            parse_field(data, reader.get(field), field)
        elif request.method in ('GET', 'DELETE'):
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
        raise RequestWarning(208, 'Already added')
    Products.objects.filter(code=data['code']).update(**data)


def delete_product(data):
    note = Products.objects.filter(
        code=data['code'],
    )

    if note.exists():
        note.delete()
    else:
        raise RequestFatal(404, 'Product not found')


def update_product(code, data):
    note = Products.objects.filter(
        code=code,
    )

    if not note.exists():
        raise RequestFatal(404, 'Product not found')
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
def product_handlers(request):
    request_type = request.method.lower()
    if request_type not in ['get', 'post', 'put', 'delete']:
        raise RequestFatal(
            405, 'expected one of {get, post, put, delete} request, got {}'.format(request_type))

    handler = globals()['product_handler_{}'.format(request_type)]
    logger.info(handler.__name__)
    return handler(request)


def product_handler_post(request):
    logger.debug("product_create")
    logger.info(request.POST)
    data = parse_data(
        request=request,
        required_params=['name', 'code', 'category'])
    # TODO: add author to data
    add_product(data)
    return 'success create with code {}'.format(data['code'])


def product_handler_delete(request):
    logger.debug("product_delete")
    data = parse_data(
        request=request,
        required_params=['code'])
    # TODO: add author to data as modifier
    delete_product(data)
    return 'success delete with code {}'.format(data['code'])


def product_handler_put(request):
    logger.debug("product_edit")
    if 'code' not in request.GET:
        raise RequestFatal(400, 'required field: code')
    code = request.GET.get('code')

    data = parse_data(
        request=request,
        optional_params=['category', 'name'])
    # TODO: add author to data as modifier
    update_product(code, data)
    return 'success put with code {}'.format(code)


def product_handler_get(request):
    logger.debug("product_info")
    if 'code' not in request.GET:
        raise RequestFatal(400, 'required field: code')
    code = request.GET.get('code')

    products = Products.objects.filter(code=code)
    if len(products) > 1:
        raise RequestFatal(500, 'More than one product with code {}'.format(code))
    if len(products) == 0:
        raise RequestFatal(404, 'Product not found')
    return get_product_json(products[0])


@access_and_errors
def products_list(request):
    logger.debug("products_list")
    check_request_type(request, 'GET')
    list_num = int(request.GET.get('list', '0'))
    list_size = int(request.GET.get('size', '100'))

    if list_size <= 0:
        raise RequestFatal(400, 'size must be more than 0')

    products = Products.objects.all().order_by('time_create')
    products_count = products.count()
    if products_count < list_num * list_size:
        return {'products': [],
                'total_count': products_count}

    products = products[list_size * list_num: list_size * (list_num + 1)]
    response = {'products': [get_product_json(product) for product in products],
                'total_count': products_count}

    if products_count > list_size * (list_num + 1):
        response.update({
            'next-url': 'database/products_list?list={}&&size={}'.format(list_num + 1, list_size)})
    return response
