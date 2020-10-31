import enum
import dataclasses
from typing import Callable
from transmission.connector_client import ConnectorClient
from .actions import *


class TaskType(enum.IntEnum):
    Periodic = 0
    Deferred = 1


class TaskState(enum.IntEnum):
    Failed = 0
    Done = 1
    Active = 2


@dataclasses.dataclass
class Task(object):
    action: Action
    connector_client: ConnectorClient
    state: TaskState = TaskState.Active

    async def update(self):
        raise NotImplementedError


class PeriodicTask(Task):
    async def update(self):
        await self.action()


class DeferredTask(Task):
    async def update(self):
        await self.action()
        self.state = TaskState.Done
