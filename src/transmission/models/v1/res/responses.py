from .handshake_response import HandshakeResponse
from .ack_response import AckResponse
from .get_device_datasheet_response import GetDeviceDatasheetResponse
from .get_device_state_response import GetDeviceStateResponse
from .get_device_value_response import GetDeviceValueResponse
from .list_devices_response import ListDevicesResponse


HEADER_TO_RESPONSE = {
    "handshake_response": HandshakeResponse,
    "ack_response": AckResponse,
    "get_device_state_response": GetDeviceStateResponse,
    "get_device_datasheet_response": GetDeviceDatasheetResponse,
    "get_sensor_value_response": GetDeviceValueResponse,
    "list_devices_response": ListDevicesResponse
}
