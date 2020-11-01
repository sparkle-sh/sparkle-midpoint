import sanic
from core.log import get_logger
from src.core.error import *
from .models import Error

log = get_logger("api.endpoint.utils")


def validate_payload(keywords, payload):
    if payload is None:
        log.warning("Received empty request")
        raise ApiError(ErrorCode.CORRUPTED_PAYLOAD, "Received empty request")
    for keyword in keywords:
        if keyword not in payload:
            log.warning(
                f"Received payload is corrupted, key {keyword} missing")
            raise ApiError(ErrorCode.CORRUPTED_PAYLOAD,
                           f'Received payload is corrupted, key {keyword} missing')
    return payload


def handle_api_exceptions(fun):
    async def wrapper(*args, **kwargs):
        try:
            return await fun(*args, **kwargs)
        except SparkleError as e:  # Cannot catch coroutine exceptions
            log.info("Catched exception when handling request: %s", e)
            return error_response(e.code, e.description)
    return wrapper


def response(model, status):
    return sanic.response.json(model.to_dict(), status=status)


def empty_response(status):
    return sanic.response.json({}, status=status)


def error_response(error_code, description=None, status_code=400):
    log.warning(f"Sending error response: {description}")
    model = Error(error_code, description)
    return response(model, status=status_code)
