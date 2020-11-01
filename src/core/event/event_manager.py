import asyncio
import aiomisc
import queue
import uuid
import copy
from src.core.error import EventError
from .event import *


class EventManager(object):
    def __init__(self):
        self.results: dict[str, dict] = {}
        self.events: dict[str, queue.PriorityQueue] = {}

    def register_service(self, ident: str):
        if self.results.get(ident) is not None or self.events.get(ident) is not None:
            raise EventError("Service already registered")
        self.results[ident] = {}
        self.events[ident] = queue.PriorityQueue()

        def event_getter():
            q = self.events.get(ident)
            if q.empty():
                return None
            return q.get()

        def event_sender(event: Event):
            destination = event.destination
            dest_queue = self.events.get(destination)
            if dest_queue is None:
                raise EventError("Invalid destination of event")
            dest_queue.put_nowait(event)
            return event.id

        def result_sender(result: Result):
            id = result.id
            destination = result.destination
            dest_dict = self.results.get(destination)
            if dest_dict is None:
                raise EventError("Invalid destination of result")
            q = dest_dict.get(id)
            if q is not None:
                raise EventError(f"Result for task {id} already sent")
            dest_dict.update({
                id: result
            })
        return EventEmitter(ident, event_sender, result_sender, event_getter, self.results[ident])


class EventEmitter(object):
    def __init__(self, ident, ev_sender, res_sender, ev_getter, results_dict):
        self.ident = ident
        self.results = results_dict
        self.ev_getter = ev_getter
        self.ev_sender = ev_sender
        self.res_sender = res_sender

    async def emit_event_to(self, destination, payload, type=EventType.INSERT_TASK, timeout=15.0):
        event_id = self.ev_sender(
            Event(self.ident, destination, payload, type))

        async def result_waiter(interval=0.1):
            while True:
                res = self.results.get(event_id)
                if res is not None:
                    return res
                await asyncio.sleep(interval)

        wait_task = asyncio.get_event_loop().create_task(result_waiter())
        try:
            res = await asyncio.wait_for(wait_task, timeout=timeout)
        except asyncio.TimeoutError as e:
            raise EventError(
                "Timeout error during waiting for event id: {}, {}".format(event_id, str(e)))
        return res

    def send_result(self, destination, payload, id):
        r = Result(self.ident, destination, payload, id)
        self.res_sender(r)

    def get_event(self):
        return self.ev_getter()
