import sanic
from src.api.controllers.agent_controller import AgentController
from src.api.controllers.device_controller import DeviceController
from .utils import *
from .models import *


def setup_device_endpoints(agent_controller: AgentController,
                           device_controller: DeviceController) -> sanic.Blueprint:
    bp = sanic.Blueprint('device', '/device')

    def validate_id(id):
        if not id.isnumeric():
            raise ApiError(ErrorCode.CORRUPTED_PAYLOAD,
                           "Device id has invalid type")
        if len(id) == 0:
            raise ApiError(ErrorCode.CORRUPTED_PAYLOAD,
                           "Device id is required")
        return int(id)

    @bp.get("/")
    @handle_api_exceptions
    async def device_get(req):
        agent_id = validate_payload(["Agent-ID"], req.headers).get('Agent-ID')
        connector_client = agent_controller.get_connector_client(
            agent_id)
        devices = await device_controller.list_devices(connector_client)
        return response(devices, 200)

    @bp.get("/<id>/state")
    @handle_api_exceptions
    async def device_state_get(req, id: str):
        agent_id = validate_payload(["Agent-ID"], req.headers).get('Agent-ID')
        id = validate_id(id)
        connector_client = agent_controller.get_connector_client(
            agent_id)
        device_state = await device_controller.get_device_state(connector_client, id)
        return response(device_state, 200)

    @bp.put("/<id>/state")
    @handle_api_exceptions
    async def device_state_put(req, id: str):
        agent_id = validate_payload(["Agent-ID"], req.headers).get('Agent-ID')
        id = validate_id(id)
        switch_device_state_query = SwitchDeviceStateQuery.from_dict(
            validate_payload(["state"], req.json))
        connector_client = agent_controller.get_connector_client(
            agent_id)
        await device_controller.switch_device_state(connector_client, id,
                                                    switch_device_state_query.state)
        return empty_response(200)

    @bp.get("/<id>/datasheet")
    @handle_api_exceptions
    async def device_datasheet_get(req, id: str):
        agent_id = validate_payload(["Agent-ID"], req.headers).get('Agent-ID')
        id = validate_id(id)
        connector_client = agent_controller.get_connector_client(
            agent_id)
        device_datasheet = await device_controller.get_device_datasheet(connector_client, id)
        return response(device_datasheet, 200)

    @bp.get("/<id>/value/<label>")
    @handle_api_exceptions
    async def device_value_get(req, id: str, label: str):
        agent_id = validate_payload(["Agent-ID"], req.headers).get('Agent-ID')
        id = validate_id(id)
        if len(label) == 0:
            raise ApiError(ErrorCode.CORRUPTED_PAYLOAD,
                           "Device label is required")
        connector_client = agent_controller.get_connector_client(
            agent_id)
        device_value = await device_controller.get_device_value(connector_client, id,
                                                                label)
        return response(device_value, 200)

    return bp
