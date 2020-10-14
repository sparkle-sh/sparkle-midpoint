import sanic
from core.log import get_logger
from .models import Error

log = get_logger("api.endpoint.util")


def generate_response(payload, default_status, Model=None):
    error = payload.get("error")
    try:
        if error:
            response = Error.from_dict(error)
            status = 400
        else:
            if Model is None:
                return sanic.response.empty(status=default_status)
            response = Model.from_dict(payload.get("content"))
            status = payload.get("status_code")
            status = default_status if not status else status
    except ValueError as e:
        return generate_error_response(error_code=400, description=str(e))
    return sanic.response.json(response.to_dict(), status=status)


def generate_error_response(error_code, description=None, status_code=400):
    response = Error(error_code, description)
    return sanic.response.json(response.to_dict(), status=status_code)
