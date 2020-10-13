import json
from typing import Dict, List
from .response import Response
from core.error import ConnectorModelError, ErrorCode


class ListDevicesResponse(Response):
    def __init__(self, payload: Dict):
        header = payload.get("header")
        if header != "list_devices_response":
            raise ConnectorModelError(
                ErrorCode.CONNECTOR_RESPONSE_ERROR, "Received unexpected response form connector")
        content = payload.get("content")
        if "devices" not in content:
            raise ConnectorModelError(
                ErrorCode.CONNECTOR_RESPONSE_ERROR, "Received unexpected broken response from connector")
        self.devices = content.get("devices")

    def get_devices(self) -> List:
        return self.devices
