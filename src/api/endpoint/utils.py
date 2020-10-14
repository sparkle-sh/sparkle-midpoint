import sanic
from core.log import get_logger
from .models import Error

log = get_logger("api.endpoint.util")


def response(model, status):
    return sanic.response.json(model.to_dict(), status=status)


def error_response(error_code, description=None, status_code=400):
    model = Error(error_code, description)
    return response(model, status=status_code)
