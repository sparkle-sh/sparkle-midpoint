import sanic


def setup_device_endpoints() -> sanic.Blueprint:
    bp = sanic.Blueprint('device', '/device')
    return bp
