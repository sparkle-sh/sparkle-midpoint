import uuid
from typing import Dict
from ..endpoint.models import Agent
from src.transmission.connector_client import ConnectorClient

class AgentController(object):
    def __init__(self):
        self.agents: Dict[str, ConnectorClient] = {}
    
    async def connect(self) -> Agent:
        agent_id = str(uuid.uuid4())
        

        return Agent(agent_id)

    async def disconnect(self, agent: Agent):
        pass
    
