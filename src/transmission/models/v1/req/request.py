from typing import Dict
from core.log import get_logger
import json

log = get_logger("connector.transmission.models.req.request")


class Request(object):
    def to_bytes(self) -> bytes:
        try:
            payload = json.dumps(self.serialize())
            return payload.encode()
        except Exception as e:
            log.warning("Error serializing request: %s", str(e))


    def serialize(self) -> Dict:
        raise NotImplementedError

