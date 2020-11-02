import aiomisc
import asyncio
import sanic
import json
from typing import Dict
from core.log import get_logger
from .agent import setup_agent_endpoints
from .device import setup_device_endpoints
from .task import setup_task_endpoints
from .utils import error_response

log = get_logger("api.endpoint.endpoint")


def setup_endpoints(app: sanic.Sanic, controllers: Dict):
    log.info("Loading endpoints")
    setup_root_endpoint(app)

    agent_controller = controllers.get("agent")
    device_controller = controllers.get("device")
    task_controller = controllers.get("task")

    log.info("Loading agent endpoints")
    app.blueprint(setup_agent_endpoints(agent_controller))

    log.info("Loading device endpoints")
    app.blueprint(setup_device_endpoints(agent_controller, device_controller))

    log.info("Loading device endpoints")
    app.blueprint(setup_task_endpoints(task_controller))

    @app.exception(sanic.exceptions.NotFound)
    async def handle_404(request, exception):
        log.warning(f"Route {request.url} not found")
        return error_response(
            400, f"Route {request.url} not found", status_code=404)

    @app.exception(sanic.exceptions.InvalidUsage)
    async def handle_invalid_usage(request, exception):
        log.warning(f"Invalid body format")
        return error_response(
            400, f"Invalid body format", status_code=400)

    @app.exception(sanic.exceptions.MethodNotSupported)
    async def handle_405(request, exception):
        log.warning(
            f"Method {request.method} not allowed for url {request.url}")
        return error_response(
            400, f"Method {request.method} not allowed for url {request.url}", status_code=405)


def setup_root_endpoint(app):
    log.info("Loading root endpoint")

    @app.get("/")
    async def root_endpoint(req):
        return sanic.response.json(get_application_info())


def get_application_info():
    payload = {
        "name": "sparkle-midpoint"
    }
    with open('./version.json', 'r') as f:
        payload["version"] = json.loads(f.read())

    return payload
