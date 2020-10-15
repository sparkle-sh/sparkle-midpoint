import uuid
from typing import Dict
from src.core.log import get_logger
from src.core.error import ConnectorError, ApiError, ErrorCode
from src.api.endpoint.models import Agent
from src.transmission.connector_client import ConnectorClient


log = get_logger("api.controllers.agent_controller")


class AgentController(object):
    def __init__(self, cfg):
        self.connector_host = cfg.connector.host
        self.connector_port = cfg.connector.port
        self.agents: Dict[str, ConnectorClient] = {}

    async def connect(self) -> Agent:
        agent_id = str(uuid.uuid4())
        connector_client = ConnectorClient(
            self.connector_host, self.connector_port)
        await connector_client.connect()
        await connector_client.initialize_session()
        self.agents.update({agent_id: connector_client})
        
        return Agent(agent_id)

    async def disconnect(self, agent: Agent):
        if agent.id not in self.agents:
            raise ApiError(ErrorCode.AGENT_NOT_EXIST, "Agent does not exist")
        connector_client = self.agents.pop(agent.id)
        await connector_client.disconnect()
