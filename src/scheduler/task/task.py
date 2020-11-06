import enum
import dataclasses
import monotonic
from typing import Callable, Dict
from transmission.connector_client import ConnectorClient
from .actions import *
from core.log import get_logger
from core.error import *

log = get_logger("scheduler.task.task")


class TaskType(enum.IntEnum):
    Periodic = 0
    Deferred = 1


class TaskState(enum.IntEnum):
    Failed = 0
    Done = 1
    Active = 2


class Task(object):
    def __init__(self, action: TaskAction, schedule: int, state: TaskState = TaskState.Active):
        self.action = action
        self.schedule = schedule
        self.state = state

    async def init(self, connector_host, connector_port):
        self.connector_client = ConnectorClient(connector_host, connector_port)
        await self.connector_client.connect()
        await self.connector_client.initialize_session()

    def get_type(self) -> TaskType:
        raise NotImplementedError

    async def deinit(self):
        await self.connector_client.disconnect()

    async def update(self):
        raise NotImplementedError

    def serialize(self) -> Dict:
        raise NotImplementedError


class PeriodicTask(Task):
    def __init__(self, action: TaskAction, interval: int):
        super().__init__(action, schedule=monotonic.monotonic() + interval)
        self.interval = interval

    def get_type(self) -> TaskType:
        return TaskType.Periodic

    async def update(self):
        try:
            succeed = await self.action.execute(self.connector_client)
            if not succeed:
                self.state = TaskState.Failed
                return
            self.schedule = monotonic.monotonic() + self.interval
        except SparkleError as e:
            log.error("Task %s failed %s", self, e)
            self.state = TaskState.Failed

    def serialize(self) -> Dict:
        return {
            'description': {
                "type": "periodic",
                "action": self.action.serialize(),
                "interval": self.interval
            },
            "status": self.state.name
        }


class DeferredTask(Task):
    def __init__(self, action: TaskAction, delay: int):
        super().__init__(action, schedule=monotonic.monotonic() + delay)
        self.delay = delay

    def get_type(self) -> TaskType:
        return TaskType.Deferred

    async def update(self):
        try:
            succeed = await self.action.execute(self.connector_client)
            if not succeed:
                self.state = TaskState.Failed
                return
            self.state = TaskState.Done
        except SparkleError as e:
            log.error("Task %s failed %s", self, e)
            self.state = TaskState.Failed

    def serialize(self) -> Dict:
        return {
            'description': {
                "type": "deferred",
                "action": self.action.serialize(),
                "delay": self.delay
            },
            "status": self.state.name
        }
