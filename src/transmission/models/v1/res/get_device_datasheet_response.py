import json
from typing import Dict
from .response import Response
from core.error import ConnectorModelError, ErrorCode


class GetDeviceDatasheetResponse(Response):
    def __init__(self, payload: Dict):
        header = payload.get("header")
        if header != "get_device_datasheet_response":
            raise ConnectorModelError(
                ErrorCode.CONNECTOR_RESPONSE_ERROR, "Received unexpected response form connector")
        content = payload.get("content")
        if "datasheet" not in content:
            raise ConnectorModelError(
                ErrorCode.CONNECTOR_RESPONSE_ERROR, "datasheet field is required")
        self.datasheet = content.get("datasheet")

    def get_datasheet(self) -> Dict:
        return self.datasheet
