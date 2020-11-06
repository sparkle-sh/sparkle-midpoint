from src.transmission.connector_client import ConnectorClient
from src.transmission.models.v1.req import *
from src.transmission.models.v1.res import *


def negator(x: int):
    return int(not x)


class TaskAction(object):
    async def execute(self, connector_client: ConnectorClient):
        raise NotImplementedError

    def serialize(self):
        raise NotImplementedError


class SwitchDeviceStateAction(TaskAction):
    def __init__(self, device_id, state_changer=negator):
        self.state_changer = state_changer
        self.device_id = device_id
        self.name = 'SwitchDeviceStateAction'

    async def execute(self, connector_client: ConnectorClient):
        req = GetDeviceStateRequest(device_id=self.device_id)
        res = await connector_client.send_request(req)
        new_state = self.state_changer(res.get_state())

        req = SwitchDeviceStateRequest(self.device_id, new_state)
        res = await connector_client.send_request(req)

        return isinstance(res, AckResponse)

    def serialize(self):
        return {
            "name": "SwitchDeviceStateAction",
            "device_id": self.device_id

        }


def string_to_action(action_str, device_id):
    return SwitchDeviceStateAction(device_id)
