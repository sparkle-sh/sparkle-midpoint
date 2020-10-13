from typing import Dict
from .request import Request


class DisconnectRequest(Request):
    def serialize(self) -> Dict:
        return {
            "header": "disconnect_request",
            "content": {
            }
        }
