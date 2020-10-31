from typing import Dict, List
from .request import Request


class GetDeviceValueRequest(Request):
    def __init__(self, device_id: int, labels: List[str]):
        self.device_id = device_id
        self.labels = labels

    def serialize(self) -> Dict:
        return {
            "header": "get_sensor_value_request",
            "content": {
                "device_id": self.device_id,
                "labels": self.labels
            }
        }
