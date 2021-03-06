import aiomisc
import asyncio
import sanic
import monotonic
from typing import Dict
import uuid
from typing import Dict
from core.log import get_logger
from core.db import ConnectionPool
from core.error import SparkleError, SchedulerError
from src.core.event.event import EventType
from .task.task import Task, TaskState, TaskType, PeriodicTask, DeferredTask
from .task.actions import *
from .db_proxy import DatabaseProxy


log = get_logger("scheduler.service")


def make_err_response(code, description) -> Dict:
    return {
        "error_code": code,
        "error_description": description
    }


class SchedulerService(aiomisc.Service):
    def __init__(self, cfg, event_manager):
        self.event_emitter = event_manager.register_service('scheduler')
        self.cfg = cfg
        self.update_job = aiomisc.PeriodicCallback(self.update)
        self.tasks: Dict[str, Task] = {}
        self.db_proxy = DatabaseProxy(self.cfg)

    async def start(self):
        log.info("Starting scheduler service")

        await self.db_proxy.init()

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

        while True:
            event = self.event_emitter.get_event()
            if event is None:
                break
            log.debug("Received event: %s", event)
            handler = task_to_handler.get(event.event_type)

            if handler is None:
                log.warning("Cannot find handler for received request")
                res = make_err_response(
                    777, "Scheduler received unknown request")
            else:
                try:
                    res = await handler(event.payload)
                except SparkleError as e:
                    log.warning("Error handling request: %s", str(e))
                    res = make_err_response(e.code, e.description)

            log.info("Sending %s to %s", res, event.sender)
            self.event_emitter.send_result(event.sender, res, event.id)

    async def update_tasks(self):
        time = monotonic.monotonic()
        for task_id, task in self.tasks.items():
            if task.state is TaskState.Active and time >= task.schedule:
                await task.update()
                await self.db_proxy.update_task_state(task.get_type(), task_id, task.state.name)

    async def insert_task(self, payload) -> Dict:
        log.debug("Inserting new task: %s", payload)
        task_type = payload.get("type")
        action = string_to_action(
            payload['action']['name'], payload['action']['device_id'])

        if task_type == 'deferred':
            task = await self.create_deferred_task(payload, action)
        else:
            task = await self.create_periodic_task(payload, action)

        await task.init(self.cfg.connector.host, self.cfg.connector.port)
        task_id = str(uuid.uuid4())
        self.tasks.update({task_id: task})

        await self.db_proxy.insert_task(task, task_id)
        log.info("Task %s added", task_id)

        return {
            'task_id': task_id
        }

    async def create_periodic_task(self, payload, action) -> Dict:
        interval = payload.get("interval")
        return PeriodicTask(action, interval)

    async def create_deferred_task(self, payload, action) -> Dict:
        delay = payload.get("delay")
        return DeferredTask(action, delay)

    async def get_task(self, payload) -> Dict:
        log.debug("Fetching task info: %s", payload)
        task_id = payload.get("task_id")

        if task_id is None:
            raise SchedulerError(777, 'Task id is missing')

        if task_id not in self.tasks:
            raise SchedulerError(777, f'Could not find task with id {task_id}')

        task = self.tasks.get(task_id)
        return task.serialize()

    async def update_task(self, payload) -> Dict:
        log.debug("Updating task: %s", payload)
        pass

    async def delete_task(self, payload) -> Dict:
        log.debug("Deleting task: %s", payload)
        task_id = payload.get("task_id")

        if task_id is None:
            raise SchedulerError(777, 'Task id is missing')

        if task_id not in self.tasks:
            log.warning('Task with id %s not found in %s', task_id, self.tasks)
            raise SchedulerError(777, f'Could not find task with id {task_id}')

        task = self.tasks.pop(task_id)

        await self.db_proxy.delete_task(task.get_type(), task_id)
        await task.deinit()

        log.info("Task %s removed", task_id)
        return {}
