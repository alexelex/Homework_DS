import logging

from django.http import HttpResponse, JsonResponse
from .exceptions import RequestFatal, RequestWarning

logger = logging.getLogger(__name__)


def access_and_errors(func):
    def wrapper(request):
        status, result = 200, None
        try:
            result = func(request)
        except RequestFatal as e:
            status = e.code
            result = e.message
            logger.warning("RequestFatal {}: {}".format(status, result))
        except RequestWarning as e:
            status = e.code
            result = e.message
            logger.info("RequestWarning {}: {}".format(status, result))
        except Exception as e:
            status = 500
            result = "error"
            logger.error("unexpected Exception: {}".format(e))

        response = {'response': result}
        return JsonResponse(response, status=status, safe=False)
    return wrapper
