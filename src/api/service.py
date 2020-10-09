import aiomisc
import asyncio
import sanic
from core.log import get_logger
from api.endpoint.endpoint import setup_endpoints 

log = get_logger("api.service")
PORT = 7776
HOST = '0.0.0.0'

class ApiService(aiomisc.Service):
    def __init__(self):
        self.port = PORT
        self.host = HOST
        self.app = sanic.Sanic(name= "sparkle-midpoint")
    
    async def start(self):
        log.info("Starting api service")
        await setup_endpoints(self.app)
        await asyncio.create_task(
            self.app.create_server(host = self.host, port = self.port, return_asyncio_server = True))
    
    async def stop(self, exception: Exception = None):
        log.info("Stopping api service")