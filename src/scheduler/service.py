import aiomisc
import asyncio
import sanic
import monotonic
from typing import Dict
import uuid
from typing import Dict
from core.log import get_logger
from core.error import SparkleError
from src.core.event.event import EventType
from .task.task import Task, TaskState, TaskType

log = get_logger("scheduler.service")


class SchedulerService(aiomisc.Service):
    def __init__(self, cfg, event_manager):
        self.event_emitter = event_manager.register_service('scheduler')
        self.cfg = cfg
        self.update_job = aiomisc.PeriodicCallback(self.update)
        self.tasks: Dict[str, Task] = {}

    async def start(self):
        log.info("Starting scheduler service")
        await self.read_tasks_from_db()
        self.update_job.start(interval=1)

    async def stop(self, exception: Exception = None):
        log.info("Stopping scheduler service")

    async def read_tasks_from_db(self):
        # to implement
        pass

    async def update(self):
        await self.read_events()
        await self.update_tasks()

    async def read_events(self):
        task_to_handler = {
            EventType.INSERT_TASK: self.insert_task,
            EventType.GET_TASK: self.get_task,
            EventType.UPDATE_TASK: self.update_task,
            EventType.DELETE_TASK: self.delete_task
        }

        log.info("Reading incoming events")
        while True:
            event = self.event_emitter.get_event()
            if event is None:
                break
            log.debug("Received event: %s", event)
            handler = task_to_handler.get(event.event_type)
            if handler is None:
                pass
                # handle this case
            res = await handler(event.payload)
            self.event_emitter.send_result(event.sender, res, event.id)

    async def update_tasks(self):
        log.info("Updating tasks")
        time = monotonic.monotonic()
        for task_id, task in self.tasks.items():
            if task.state is TaskState.Active and time >= task.schedule:
                await task.update()

            if task.state is TaskState.Done:
                self.tasks.pop(task_id)

    def insert_task(self, payload) -> Dict:
        pass

    def get_task(self, payload) -> Dict:
        pass

    def update_task(self, payload) -> Dict:
        pass

    def delete_task(self, payload) -> Dict:
        pass
