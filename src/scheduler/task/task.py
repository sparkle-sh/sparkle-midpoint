import enum
import dataclasses
import monotonic
from typing import Callable, Dict
from transmission.connector_client import ConnectorClient
from .actions import *


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

    async def deinit(self):
        await self.connector_client.disconnect()

    async def update(self):
        raise NotImplementedError

    async def serialize(self) -> Dict:
        raise NotImplementedError


class PeriodicTask(Task):
    def __init__(self, action: TaskAction, interval: int):
        super().__init__(action, schedule=monotonic.monotonic() + interval)
        self.interval = interval

    async def update(self):
        succeed = await self.action.execute(self.connector_client)
        print("xd1")
        if not succeed:
            self.state = TaskState.Failed
            print("Xd2")
            return
        self.schedule = monotonic.monotonic() + self.interval


class DeferredTask(Task):
    def __init__(self, action: TaskAction, delay: int):
        super().__init__(action, schedule=monotonic.monotonic() + delay)
        self.delay = delay

    async def update(self):
        succeed = await self.action.execute(self.connector_client)
        if not succeed:
            self.state = TaskState.Failed
            return
        self.state = TaskState.Done
