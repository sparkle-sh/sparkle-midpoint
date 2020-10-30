import json
from typing import Dict
from .response import Response
from core.error import ConnectorModelError, ErrorCode


class GetDeviceStateResponse(Response):
    def __init__(self, payload: Dict):
        header = payload.get("header")
        if header != "get_device_state_response":
            raise ConnectorModelError(
                ErrorCode.CONNECTOR_RESPONSE_ERROR, "Received unexpected response form connector")
        content = payload.get("content")
        if "state" not in content:
            raise ConnectorModelError(
                ErrorCode.CONNECTOR_RESPONSE_ERROR, "state field is required")
        self.state = content.get("state")

    def get_state(self) -> int:
        return self.state.get("state_value")
