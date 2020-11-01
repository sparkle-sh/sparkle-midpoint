from core.event import event


class TaskController(object):
    def __init__(self, event_emitter):
        self.event_emitter = event_emitter

    async def get_task(self, task_id):
        payload = {
            'task_id': task_id
        }
        response = await self.event_emitter.emit_event_to('scheduler', payload, EventType.GET_TASK)

    async def insert_task(self):
        pass

    async def update_task(self):
        pass

    async def delete_task(self, task_id):
        payload = {
            'task_id': task_id
        }
        response = await self.event_emitter.emit_event_to('scheduler', payload, EventType.DELETE_TASK)
