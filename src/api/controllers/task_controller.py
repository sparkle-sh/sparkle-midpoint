from src.core.event import event
from src.core.error import ApiError
from src.api.endpoint.models import TaskDescription, TaskId, Task
from src.api.endpoint.utils import *


def handle_scheduler_error(response):
    if 'error_code' in response.payload:
        raise ApiError(
            response.payload['error_code'], response.payload['error_description'])


class TaskController(object):
    def __init__(self, event_emitter):
        self.event_emitter = event_emitter

    async def get_task(self, task_id):
        payload = {
            'task_id': task_id
        }
        response = await self.event_emitter.emit_event_to('scheduler', payload, event.EventType.GET_TASK)
        handle_scheduler_error(response)
        return Task.from_dict(response.payload)

    async def insert_task(self, task: TaskDescription):
        payload = task.to_dict()
        response = await self.event_emitter.emit_event_to('scheduler', payload, event.EventType.INSERT_TASK)
        handle_scheduler_error(response)
        return TaskId.from_dict(response.payload)

    async def update_task(self):
        pass

    async def delete_task(self, task_id):
        payload = {
            'task_id': task_id
        }
        response = await self.event_emitter.emit_event_to('scheduler', payload, event.EventType.DELETE_TASK)
        handle_scheduler_error(response)
