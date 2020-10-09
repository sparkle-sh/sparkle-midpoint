import signal
import os
import uvloop
import asyncio
import aiomisc
from core.log import get_logger
from api.service import ApiService

log = get_logger("main")


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

api_service = ApiService()

with aiomisc.entrypoint(api_service, log_config= False) as loop:
    log.info("Starting event loop")
    loop.run_forever()