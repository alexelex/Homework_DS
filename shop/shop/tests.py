import json

from django.test import TestCase
from django.test.client import Client


class ToolsTests(TestCase):
    FIELDS = ['code', 'category', 'name', 'author', 'modifier']

    DATA_CREATE = [
        {
            'status': 200,
            'data': {
                'name': '1',
                'code': '1',
                'category': '1',
            }
        },
        {
            'status': 208,
            'data': {
                'name': '2',
                'code': '1',
                'category': '3'
            }
        },
        {
            'status': 400,
            'data': {},
        },
        {
            'status': 400,
            'data': {
                'name': '1',
                'code': '2'
            }
        },
        {
            'status': 400,
            'data': {
                'name': '1',
                'category': '1'
            }
        },
        {
            'status': 400,
            'data': {
                'category': '1',
                'code': '2'
            }
        },
    ]

    DATA_DELETE = [
        {
            'status': 400,
            'params_string': '',
        },
        {
            'status': 404,
            'params_string': '?code=2',
        },
        {
            'status': 200,
            'params_string': '?code=1',
        },
        {
            'status': 404,
            'params_string': '?code=1',
        },
    ]

    DATA_EDIT = [
        {
            'status': 400,
            'params_string': '',
            'data': {},
        },
        {
            'status': 404,
            'params_string': '?code=2',
            'data': {},
        },
        {
            'status': 200,
            'params_string': '?code=1',
            'data': {},
        },
        {
            'status': 200,
            'params_string': '?code=1',
            'data': {
                'name': '3',
                'category': '15',
            },
        },
        {
            'status': 200,
            'params_string': '?code=1',
            'data': {
                'name': '4',
                'category': '15',
            },
        },
        {
            'status': 200,
            'params_string': '?code=1',
            'data': {
                'name': '5',
            },
        },
    ]

    RESULT_LIST = {
        'create': [
            {
                'name': '1',
                'code': '1',
                'category': '1',
            },
        ],
        'edit': [
            {
                'name': '5',
                'code': '1',
                'category': '15',
            },
        ]
    }

    DATA = [
        {
            'name': '1',
            'code': '1',
            'category': '1',
        },
        {
            'name': '2',
            'code': '2',
            'category': '2',
        }
    ]

    def get_response(self, url, request_type, data={}, status=200, params_string=''):
        c = Client()
        request_url = '/database/' + url + params_string

        if request_type == 'post':
            response = c.post(
                request_url,
                data,
            )
        elif request_type == 'get':
            response = c.get(
                request_url,
                data,
            )
        elif request_type == 'delete':
            response = c.delete(
                request_url,
                data,
            )
        elif request_type == 'put':
            response = c.put(
                request_url,
                data,
            )

        self.assertEqual(status, response.status_code)
        if response.content and status == 200:
            return json.loads(response.content)

    def check_result(self, product, expected):
        for field in self.FIELDS:
            self.assertEqual(product.get(field), expected.get(field))

    def check_result_list(self, products, expected_products,
                          next_url=None, expected_next_url=None):
        self.assertEqual(len(products), len(expected_products))
        self.assertEqual(next_url, expected_next_url)
        for product, expected in zip(products, expected_products):
            for field in self.FIELDS:
                self.assertEqual(product.get(field), expected.get(field))

    def test_create_tool(self):
        for data in self.DATA_CREATE:
            self.get_response(
                data=data['data'],
                url='product/create',
                request_type='post',
                status=data['status'],
            )

        self.get_response(
            data=self.DATA_CREATE[0]['data'],
            url='product/create',
            request_type='get',
            status=400,
        )
        response = self.get_response(
            url='products_list',
            request_type='get',
        )
        self.check_result_list(response['products'], self.RESULT_LIST['create'])

        response = self.get_response(
            url='product',
            request_type='get',
            params_string='?code={}'.format(self.RESULT_LIST['create'][0]['code']),
        )
        self.check_result(response, self.RESULT_LIST['create'][0])

    def test_delete_tool(self):
        for data in self.DATA_CREATE:
            self.get_response(
                data=data['data'],
                url='product/create',
                request_type='post',
                status=data['status'],
            )

        for request_type in ('get', 'post', 'put',):
            self.get_response(
                params_string='?code=1',
                url='product/delete',
                request_type=request_type,
                status=400,
            )

        for data in self.DATA_DELETE:
            self.get_response(
                params_string=data['params_string'],
                url='product/delete',
                request_type='delete',
                status=data['status'],
            )

        response = self.get_response(
            url='products_list',
            request_type='get',
        )
        self.check_result_list(response['products'], [])

        self.get_response(
            url='product',
            request_type='get',
            params_string='?code={}'.format(self.RESULT_LIST['create'][0]['code']),
            status=404
        )

    def test_edit_tool(self):
        self.get_response(
            data=self.DATA_CREATE[0]['data'],
            url='product/create',
            request_type='post',
            status=self.DATA_CREATE[0]['status'],
        )

        response = self.get_response(
            url='products_list',
            request_type='get',
        )
        self.check_result_list(response['products'], self.RESULT_LIST['create'])

        response = self.get_response(
            url='product',
            request_type='get',
            params_string='?code={}'.format(self.RESULT_LIST['create'][0]['code']),
        )
        self.check_result(response, self.RESULT_LIST['create'][0])

        for request_type in ('get', 'post', 'delete',):
            self.get_response(
                params_string='?code=1',
                url='product/edit',
                request_type=request_type,
                status=400,
            )

        for data in self.DATA_EDIT[4:]:
            self.get_response(
                params_string=data['params_string'],
                data=data['data'],
                url='product/edit',
                request_type='put',
                status=data['status'],
            )

        response = self.get_response(
            url='products_list',
            request_type='get',
        )
        self.check_result_list(response['products'], self.RESULT_LIST['edit'])

        response = self.get_response(
            url='product',
            request_type='get',
            params_string='?code={}'.format(self.RESULT_LIST['edit'][0]['code']),
        )
        self.check_result(response, self.RESULT_LIST['edit'][0])

        response = self.get_response(
            url='product',
            request_type='get',
            status=400,
        )

        response = self.get_response(
            url='product',
            request_type='get',
            params_string='?code={}'.format('100'),
            status=404,
        )

    def test_list_tool(self):
        for data in self.DATA:
            self.get_response(
                data=data,
                url='product/create',
                request_type='post',
            )

        response = self.get_response(
            url='products_list',
            request_type='get',
        )
        self.check_result_list(response['products'], self.DATA)

        response = self.get_response(
            url='products_list',
            request_type='get',
            params_string='?size=1',
        )
        self.check_result_list(
            response['products'],
            [self.DATA[0]],
            response.get('next-url'),
            'database/products_list?list=1&&size=1'
        )

        response = self.get_response(
            url='products_list',
            request_type='get',
            params_string='?list=1&&size=1',
        )
        self.check_result_list(
            response['products'],
            [self.DATA[1]],
            response.get('next-url'),
        )
