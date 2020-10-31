from src.transmission.connector_client import ConnectorClient


class Action(object):
    def execute(self, connector_client: ConnectorClient):
        raise NotImplementedError


class SwitchDeviceStateAction(Action):
    def __init__(self, state_changer):
        self.state_changer = state_changer

    def execute(self, connector_client: ConnectorClient):
        pass
