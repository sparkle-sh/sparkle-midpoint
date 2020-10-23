import asyncio
import struct
import json
import functools
from src.core.error import ConnectorError, ErrorCode
from .models.v1.res import Response, HEADER_TO_RESPONSE
from .models.v1.req.request import Request
from core.log import get_logger

log = get_logger("transmission.transmitter")

PAYLOAD_LENGTH_BYTES = 4


def catch_os_error(msg):
    def inner(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except OSError as e:
                log.warning(f"Connector error has occured: {msg}")
                raise ConnectorError(ErrorCode.CONNECTOR_ERROR, msg)
        return wrapper
    return inner


class Transmitter(object):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @catch_os_error("Connection refused, connector is down")
    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    @catch_os_error("Connector dropped connection before disconnecting")
    async def disconnect(self):
        self.writer.close()
        await self.writer.wait_closed()

    @catch_os_error("Could not send request, connector dropped connection")
    async def send_request(self, req: Request) -> None:
        await self.send_payload(req.to_bytes())

    @catch_os_error("Could read response, connector dropped connection")
    async def read_response(self) -> Response:
        payload = await self.read_payload()

        j = json.loads(payload)
        response_builder = HEADER_TO_RESPONSE.get(j.get("header"))
        if response_builder is not None:
            return response_builder(j)
        raise ConnectorError(ErrorCode.CONNECTOR_ERROR,
                             "Unknown connector response")

    async def send_payload(self, req: bytes) -> None:
        await self.send_payload_length(len(req))
        self.writer.write(req)
        await self.writer.drain()

    async def send_payload_length(self, length: int) -> None:
        payload = struct.pack("i", length)
        self.writer.write(payload)
        await self.writer.drain()

    async def read_payload(self) -> str:
        length = await self.read_payload_length()
        payload = await self.reader.read(*length)
        return payload.decode()

    async def read_payload_length(self) -> int:
        b = await self.reader.read(PAYLOAD_LENGTH_BYTES)
        return struct.unpack("i", b)
