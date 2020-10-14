import sanic
from ..controlers.agent_controller import AgentController
from .utils import *
from .models import Agent


def setup_agent_endpoints(agent_controller: AgentController):
    bp = sanic.Blueprint('agent', url_prefix='/agent')

    @bp.post("/")
    async def agent_post(req):
        agent = await agent_controller.connect()
        return response(agent, 201)

    @bp.delete("/")
    async def agent_delete(req):
        return sanic.response.json({"hello": "delete"})

    return bp
