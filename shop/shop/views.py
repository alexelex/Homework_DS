# -*- coding: utf-8 -*-#
import json

from shop.decorators import access_and_errors
from shop.models import Products
from shop.exceptions import RequestFatal, RequestWarning


def parse_field(data, var, name, to_dict=False):
    if var is not None:
        if to_dict:
            try:
                var = json.loads(var)
            except ValueError:
                return
        data.update({name: var})


def parse_data(request, required_params, optional_params):
    data = {}

    for field in required_params + optional_params:
        parse_field(data, request.POST.get(field), field)

    for field in required_params:
        if field not in data:
            raise RequestFatal(
                400, 'Bad Request: required field {}'.format(field))
    return data


def check_request_type(request, request_type):
    if request.method != request_type:
        raise RequestFatal(
            400, 'Bad Request: expected {} request'.format(request_type))


def add_product(data):
    note, created = Products.objects.get_or_create(
        code=data['code'],
    )

    if not created:
        raise RequestWarning(208, 'Already Reported')
    Products.objects.filter(code=data['code']).update(**data)


def delete_product(data):
    note = Products.objects.filter(
        code=data['code'],
    )

    if note.exists():
        note.delete()
    else:
        raise RequestWarning(208, 'Already Reported')


def update_product(data):
    note = Products.objects.filter(
        code=data['code'],
    )

    if not note.exists():
        raise RequestFatal(404, 'Not Found')
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
    check_request_type(request, 'POST')
    data = parse_data(
        request=request,
        required_params=['name', 'code', 'category'])
    # TODO: add author to data
    add_product(data)


@access_and_errors
def product_delete(request):
    check_request_type(request, 'POST')
    data = parse_data(
        request=request,
        required_params=['code'])
    # TODO: add author to data as modifier
    delete_product(data)


@access_and_errors
def product_edit(request):
    check_request_type(request, 'POST')
    data = parse_data(
        request=request,
        required_params=['code'],
        optional_params=['category', 'name'])
    # TODO: add author to data as modifier
    update_product(data)


@access_and_errors
def products_list(request):
    check_request_type(request, 'GET')
    list_num = int(request.GET.get('list', '0'))


@access_and_errors
def product_info(request):
    check_request_type(request, 'GET')
    if 'code' not in request.GET:
        raise RequestFatal(400, 'Bad Request: required field code')
    code = request.GET.get('code')

    products = Products.objects.filter(code=code)
    if len(products) > 1:
        raise RequestFatal(500, 'More than one product with code {}'.format(code))
    if len(products) == 0:
        raise RequestFatal(404, 'Not Found')
    return get_product_json(products[0])
