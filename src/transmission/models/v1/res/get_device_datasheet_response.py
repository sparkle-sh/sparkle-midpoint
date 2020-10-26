import json
from typing import Dict
from .response import Response
from src.transmission.models.v1.device_type import DeviceType
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
        if 'labels' in self.datasheet:
            self.device_type = DeviceType.SENSOR
        elif 'values' in self.datasheet:
            self.device_type = DeviceType.SWITCHABLE
        else:
            raise ConnectorModelError(
                ErrorCode.CONNECTOR_RESPONSE_ERROR, "invalid device type")

    def get_device_type(self) -> DeviceType:
        return self.device_type

    def get_datasheet(self) -> Dict:
        return self.datasheet
