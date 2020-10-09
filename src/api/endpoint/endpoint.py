import aiomisc
import asyncio
import sanic
import json
from core.log import get_logger

log = get_logger("api.endpoint.endpoint")

async def setup_endpoints(app: sanic.Sanic):
    log.info("Loading endpoints")
    await setup_root_endpoint(app)


async def setup_root_endpoint(app):
    log.info("Loading root endpoint")
    @app.get("/")
    async def root_endpoint(req):
        return sanic.response.json(get_application_info())


def get_application_info():
    payload = {
        "name": "sparkle-midpoint"
    }
    with open ('./VERSION.json','r') as f:
        payload["version"] = json.loads(f.read())
    
    return payload

