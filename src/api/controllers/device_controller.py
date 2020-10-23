from src.transmission.models.v1.req import ListDevicesRequest
from src.transmission.models.v1.res import ListDevicesResponse
from src.transmission.connector_client import ConnectorClient
from src.core.error import ErrorCode, ApiError
from src.api.endpoint.models import Devices, Device


class DeviceController(object):
    async def list_devices(self, connector_client: ConnectorClient):
        res = await connector_client.send_request(ListDevicesRequest())
        if not isinstance(res, ListDevicesResponse):
            raise ApiError(ErrorCode.CONNECTOR_RESPONSE_ERROR,
                           "Received unexpected response from connector")
        devices = [Device.from_dict(d) for d in res.get_devices()]
        return Devices(devices=devices)
