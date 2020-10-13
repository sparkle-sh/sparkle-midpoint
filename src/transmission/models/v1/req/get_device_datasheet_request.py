from typing import Dict
from .request import Request


class GetDeviceDatasheetRequest(Request):
    def __init__(self, device_id: int):
        self.device_id = device_id

    def serialize(self) -> Dict:
        return {
            "header": "get_device_datasheet_request",
            "content": {
                "device_id": self.device_id
            }
        }
