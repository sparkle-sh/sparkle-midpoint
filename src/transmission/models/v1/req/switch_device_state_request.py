from typing import Dict
from .request import Request


class SwitchDeviceStateRequest(Request):
    def __init__(self, device_id, state):
        self.device_id = device_id
        self.state = state

    def serialize(self) -> Dict:
        return {
            "header": "switch_device_state_request",
            "content": {
                "device_id": self.device_id,
                "state": self.state
            }
        }
