import json
from typing import Dict
from .response import Response
from core.error import ConnectorModelError, ErrorCode


class GetDeviceValueResponse(Response):
    def __init__(self, payload: Dict):
        header = payload.get("header")
        if header != "get_sensor_value_response":
            raise ConnectorModelError(
                ErrorCode.CONNECTOR_RESPONSE_ERROR, "Received unexpected response form connector")
        content = payload.get("content")
        if "values" not in content:
            raise ConnectorModelError(
                ErrorCode.CONNECTOR_RESPONSE_ERROR, "value field is required")
        self.values = content.get("values")

    def get_values(self) -> Dict:
        return self.values
