import asyncio
from .transmitter import Transmitter
from .models.v1.req import *
from .models.v1.res import *
from .models.v1.req.request import Request
from .models.v1.res.response import Response
from core.error import ConnectorError, ErrorCode
from core.log import get_logger

log = get_logger("transmission.connector_client")


class ConnectorClient(object):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.transmitter = Transmitter(host, port)
        self.lock = asyncio.Lock()

    @staticmethod
    async def spawn(host: str, port: int):
        c = ConnectorAgent(host, port)
        await c.connect()
        return c

    async def send_request(self, request: Request) -> Response:
        async with self.lock:
            await self.transmitter.send_request(request)
            res = await self.transmitter.read_response()
            return res

    async def connect(self):
        await self.transmitter.connect()

    async def disconnect(self):
        res = await self.send_request(DisconnectRequest())
        try:
            if not isinstance(res, AckResponse):
                log.warning("Error during agent disconnection")
                raise ConnectorError(
                    ErrorCode.CONNECTOR_ERROR, "error during agent disconnection")
        finally:
            await self.transmitter.disconnect()

    async def initialize_session(self):
        await self.transmitter.send_request(HandshakeRequest())
        res = await self.transmitter.read_response()
        if not isinstance(res, HandshakeResponse):
            log.warning("Received invalid handshake from sparkle-connector")
            raise ConnectorError(ErrorCode.INVALID_HANDSHAKE,
                                 "received invalid handshake from sparkle-connector")
