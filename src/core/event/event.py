import dataclasses
import uuid
import enum
from typing import Dict


class EventType(enum.IntEnum):
    INSERT_TASK = 0
    GET_TASK = 1
    UPDATE_TASK = 2
    DELETE_TASK = 3


@dataclasses.dataclass
class Event(object):
    sender: str
    destination: str
    payload: Dict
    event_type: EventType = EventType.INSERT_TASK
    id: uuid.UUID = uuid.uuid4()

    def __str__(self) -> str:
        return f'<Event: {self.sender}/{self.destination}/{self.event_type}/{self.id}>\n{self.payload}'

    def __hash__(self):
        return hash(self.id)


@dataclasses.dataclass
class Result(object):
    sender: str
    destination: str
    payload: Dict
    id: uuid.UUID
