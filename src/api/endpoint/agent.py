import sanic
from src.api.controllers.agent_controller import AgentController
from .utils import *
from .models import Agent


def setup_agent_endpoints(agent_controller: AgentController):
    bp = sanic.Blueprint('agent', url_prefix='/agent')

    @bp.post("/")
    @handle_api_exceptions
    async def agent_post(req):
        agent = await agent_controller.connect()
        return response(agent, 201)

    @bp.delete("/")
    @handle_api_exceptions
    async def agent_delete(req):
        agent = Agent.from_dict(validate_payload(['id'], req.json))
        await agent_controller.disconnect(agent)
        return empty_response(200)
            
    return bp
