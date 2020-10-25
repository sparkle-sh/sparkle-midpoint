from src.transmission.models.v1.req import *
from src.transmission.models.v1.res import * 
from src.transmission.connector_client import ConnectorClient
from src.core.error import ErrorCode, ApiError
from src.api.endpoint.models import Devices, Device, DeviceState


class DeviceController(object):
    async def list_devices(self, connector_client: ConnectorClient):
        res = await connector_client.send_request(ListDevicesRequest())
        if not isinstance(res, ListDevicesResponse):
            raise ApiError(ErrorCode.CONNECTOR_RESPONSE_ERROR,
                           "Received unexpected response from connector")
        devices = [Device.from_dict(d) for d in res.get_devices()]
        return Devices(devices=devices)

    async def get_device_state(self, connector_client: ConnectorClient, device_id: int):
        res = await connector_client.send_request(GetDeviceStateRequest(device_id))
        if not isinstance(res, GetDeviceStateResponse):
            raise ApiError(ErrorCode.CONNECTOR_RESPONSE_ERROR,
                           "Received unexpected response from connector")
        return DeviceState(state_value=res.get_state())
    
    async def switch_device_state(self, connector_client: ConnectorClient, device_id: int, state: DeviceState):
        res = await connector_client.send_request(SwitchDeviceStateRequest(device_id, state.state_value))
        if not isinstance(res, AckResponse):
            raise ApiError(ErrorCode.CONNECTOR_RESPONSE_ERROR,
                           "Received unexpected response from connector")

        
