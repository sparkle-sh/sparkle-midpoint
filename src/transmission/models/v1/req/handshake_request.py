from typing import Dict
from .request import Request


class HandshakeRequest(Request):
    def serialize(self) -> Dict:
        return {
            "header": "handshake_request",
            "content": {
                "session_type": "agent"
            }
        }
