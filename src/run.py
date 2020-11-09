import signal
import os
import uvloop
import asyncio
import aiomisc
from core.log import get_logger
from core import config
from core.db import ConnectionPool
from core.event.event_manager import EventManager
from api.service import ApiService
from scheduler.service import SchedulerService

log = get_logger("main")

log.info("Loading config")
config = config.Config("./cfg/config.json")
log.info("Config loaded")


@aiomisc.receiver(aiomisc.entrypoint.PRE_START)
async def pre_init(entrypoint, services):
    log.info("Setting up signal handler")

    async def shutdown() -> None:
        log.info("Received SIGINT/SIGTERM shutting down all active task")
        tasks = [t for t in asyncio.Task.all_tasks(
        ) if t is not asyncio.Task.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        log.info("Stopping event loop")
        asyncio.get_event_loop().stop()

    for sig in [signal.SIGTERM, signal.SIGINT]:
        asyncio.get_event_loop().add_signal_handler(
            sig, lambda: asyncio.create_task(shutdown())
        )

event_manager = EventManager()

log.info("Creating services instances")
services = [
    ApiService(config, event_manager), SchedulerService(config, event_manager)
]
log.info("Services instances created")

log.info("Installing uvloop")
uvloop.install()

with aiomisc.entrypoint(*services, log_config=False) as loop:
    log.info("Starting event loop")
    loop.run_forever()
