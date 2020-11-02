import sanic
from src.api.controllers.task_controller import TaskController
from .utils import *
from .models import TaskId, TaskUpdate, Task, TaskDescription


def setup_task_endpoints(task_controller: TaskController):
    bp = sanic.Blueprint('task', url_prefix='/task')

    @bp.post("/")
    @handle_api_exceptions
    async def task_post(req):
        task_description = TaskDescription.from_dict(
            validate_payload(['type', 'action'], req.json))
        res = await task_controller.insert_task(task_description)
        return response(res, 201)

    @bp.get("/")
    @handle_api_exceptions
    async def task_get(req):
        task_id = TaskId.from_dict(
            validate_payload(['task_id'], req.json)).task_id
        res = await task_controller.get_task(task_id)
        return response(res, 200)

    @bp.put("/")
    @handle_api_exceptions
    async def task_update(req):
        pass

    @bp.delete("/")
    @handle_api_exceptions
    async def task_delete(req):
        task_id = TaskId.from_dict(
            validate_payload(['task_id'], req.json)).task_id
        await task_controller.delete_task(task_id)
        return empty_response(200)

    return bp
