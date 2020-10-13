from typing import Dict
from .request import Request


class ListDevicesRequest(Request):
    def serialize(self) -> Dict:
        return {
            "header": "list_devices_request",
            "content": {}
        }
