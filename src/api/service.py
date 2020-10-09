import aiomisc
import asyncio
import sanic
import typing
from core.log import get_logger
from api.endpoint.endpoint import setup_endpoints 

log = get_logger("api.service")


class ApiService(aiomisc.Service):
    def __init__(self, cfg):
        self.cfg = cfg
        self.app = sanic.Sanic(name= "sparkle-api-gateway")
    
    async def start(self):
        log.info("Starting api service")
        await setup_endpoints(self.app)
        await asyncio.create_task(
            self.app.create_server(host=self.cfg.api.host, port=self.cfg.api.port, return_asyncio_server = True))
    
    async def stop(self, exception: Exception = None):
        log.info("Stopping api service")