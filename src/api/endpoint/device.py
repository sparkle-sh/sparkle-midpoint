import sanic
from ..controllers.agent_controller import AgentController
from ..controllers.device_controller import DeviceController
from .utils import *
from .models import Agent


def setup_device_endpoints(agent_controller: AgentController,
                           device_controlller: DeviceController) -> sanic.Blueprint:
    bp = sanic.Blueprint('device', '/device')

    @bp.get("/")
    @handle_api_exceptions
    async def device_get(req):
        agent = Agent.from_dict(validate_payload(['id'], req.json))
        connector_client = agent_controller.get_connection_client(agent)
        devices = await device_controlller.list_devices(connector_client)
        return response(devices, 200)

    return bp
