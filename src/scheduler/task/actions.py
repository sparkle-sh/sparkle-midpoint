from src.transmission.connector_client import ConnectorClient
from src.transmission.models.v1.req import *
from src.transmission.models.v1.res import *


class TaskAction(object):
    def execute(self, connector_client: ConnectorClient):
        raise NotImplementedError


class SwitchDeviceStateAction(TaskAction):
    def __init__(self, state_changer, device_id):
        self.state_changer = state_changer
        self.device_id = device_id

    async def execute(self, connector_client: ConnectorClient):
        req = SwitchDeviceStateRequest(self.device_id, 1)
        res = await connector_client.send_request(req)
        print(res)
        return True


def string_to_action(action_str, device_id):
    return SwitchDeviceStateAction(None, device_id)
