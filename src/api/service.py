import aiomisc
import asyncio
import sanic
import typing
from core.log import get_logger
from core.error import SparkleError
from api.endpoint.endpoint import setup_endpoints
from api.controllers import agent_controller
from api.endpoint.utils import handle_api_exceptions


log = get_logger("api.service")


class ApiService(aiomisc.Service):
    def __init__(self, cfg):
        self.cfg = cfg
        self.app = sanic.Sanic(name="sparkle-midpoint")
        self.controllers = {
            'agent': agent_controller.AgentController(self.cfg)
        }

    async def start(self):
        log.info("Starting api service")
        setup_endpoints(self.app, self.controllers)
        await asyncio.create_task(
            self.app.create_server(host=self.cfg.api.host, port=self.cfg.api.port, return_asyncio_server=True))

    async def stop(self, exception: Exception = None):
        log.info("Stopping api service")
