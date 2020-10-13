from . import *


HEADER_TO_RESPONSE = {
    "handshake_response": HandshakeResponse,
    "ack_response": AckResponse,
    "get_device_state_response": GetDeviceStateResponse,
    "get_device_datasheet_response": GetDeviceDatasheetResponse,
    "get_sensor_value_response": GetSensorValueResponse,
    "list_devices_response": ListDevicesResponse
}
