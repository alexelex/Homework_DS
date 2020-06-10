import json
from .exceptions import RequestFatal

def parse_field(data, var, name, to_dict=False):
    if var is not None:
        if to_dict:
            try:
                var = json.loads(var)
            except ValueError:
                return
        data.update({name: var})

def get_reader(request):
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
    return reader


def parse_data(request, required_params=[]):
    data = {}
    if request.method in ('PUT', 'POST'):
        reader = get_reader(request)

    for field in required_params:
        if request.method in ('PUT', 'POST'):
            parse_field(data, reader.get(field), field)
        elif request.method in ('GET', 'DELETE'):
            parse_field(data, request.GET.get(field), field)

    for field in required_params:
        if field not in data:
            raise RequestFatal(
                400, 'required field: {}'.format(field))
    return data
