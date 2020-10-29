import sanic
from src.api.controllers.agent_controller import AgentController
from src.api.controllers.device_controller import DeviceController
from .utils import *
from .models import *


def setup_device_endpoints(agent_controller: AgentController,
                           device_controller: DeviceController) -> sanic.Blueprint:
    bp = sanic.Blueprint('device', '/device')

    @bp.get("/")
    @handle_api_exceptions
    async def device_get(req):
        agent_query = AgentQuery.from_dict(validate_payload(["agent"], req.json))
        connector_client = agent_controller.get_connection_client(agent_query.agent)
        devices = await device_controller.list_devices(connector_client)
        return response(devices, 200)

    @bp.get("/state")
    @handle_api_exceptions
    async def device_state_get(req):
        keywords = ["device_id", "agent"]
        device_query = DeviceQuery.from_dict(validate_payload(keywords, req.json))
        connector_client = agent_controller.get_connection_client(device_query.agent)
        device_state = await device_controller.get_device_state(connector_client, device_query.device_id)
        return response(device_state, 200)

    @bp.put("/state")
    @handle_api_exceptions
    async def device_state_put(req):
        keywords = ["device_id", "agent", "state"]
        switch_device_state_query = SwitchDeviceStateQuery.from_dict(validate_payload(keywords, req.json))
        connector_client = agent_controller.get_connection_client(switch_device_state_query.agent)
        await device_controller.switch_device_state(connector_client, switch_device_state_query.device_id, 
            switch_device_state_query.state)
        return empty_response(200)

    return bp