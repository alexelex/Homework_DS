from django.http import JsonResponse

from shop.exceptions import RequestFatal, RequestWarning


def access_and_errors(func):
    def wrapper(request):
        result = {}
        status = 200
        try:
            result = func(request)
        except RequestFatal as e:
            status = e.code
            result = {'error': e.message}
        except RequestWarning as e:
            status = e.code
            result = {'warning': e.message}
        except Exception as e:
            status = 500
            result = {'error': e.message}
        return JsonResponse(result, status=status)
    return wrapper
