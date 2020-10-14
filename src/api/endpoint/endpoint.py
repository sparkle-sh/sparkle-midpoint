import aiomisc
import asyncio
import sanic
import json
from typing import Dict
from core.log import get_logger
from .agent import setup_agent_endpoints
from .device import setup_device_endpoints

log = get_logger("api.endpoint.endpoint")


def setup_endpoints(app: sanic.Sanic, controllers: Dict):
    log.info("Loading endpoints")
    setup_root_endpoint(app)

    log.info("Loading agent endpoints")
    app.blueprint(setup_agent_endpoints(controllers.get('agent')))

    log.info("Loading device endpoints")
    app.blueprint(setup_device_endpoints())


def setup_root_endpoint(app):
    log.info("Loading root endpoint")

    @app.get("/")
    async def root_endpoint(req):
        return sanic.response.json(get_application_info())


def get_application_info():
    payload = {
        "name": "sparkle-midpoint"
    }
    with open('./VERSION.json', 'r') as f:
        payload["version"] = json.loads(f.read())

    return payload
