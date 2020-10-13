import json
from typing import Dict
from .response import Response
from core.error import ConnectorModelError, ErrorCode


class AckResponse(Response):
    def __init__(self, payload: Dict):
        header = payload.get("header")
        if header != "ack_response":
            raise ConnectorModelError(
                ErrorCode.CONNECTOR_RESPONSE_ERROR, "Received unexpected response form connector")
