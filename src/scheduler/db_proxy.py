from src.core.db import ConnectionPool
from src.scheduler.task.task import TaskType


class DatabaseProxy(object):
    def __init__(self, cfg):
        self.cfg = cfg

    async def init(self):
        await ConnectionPool.init(self.cfg)

    async def insert_task(self, task, uuid):
        task_type = task.get_type()

        q = "INSERT INTO {}_tasks (task_id, device_id, action, {}, status) VALUES ($1, $2, $3, $4, $5)"
        type_string, time_table = (
            'periodic', 'interval') if task_type == TaskType.Periodic else ('deferred', 'delay')
        action = task.action.serialize().get('name')

        async with ConnectionPool.acquire_connection() as conn:
            await conn.execute(q.format(type_string, time_table),
                               uuid, task.action.device_id, action, getattr(task, time_table), task.state.name)

    async def delete_task(self, task_type, task_id):
        table = 'periodic' if task_type == TaskType.Periodic else 'deferred'
        q = f"DELETE FROM {table}_tasks WHERE task_id=$1"

        async with ConnectionPool.acquire_connection() as conn:
            await conn.execute(q, task_id)

    async def update_task_state(self, task_type, task_id, state):
        table = 'periodic' if task_type == TaskType.Periodic else 'deferred'
        q = f"UPDATE {table}_tasks SET status=$1 WHERE task_id=$2"

        async with ConnectionPool.acquire_connection() as conn:
            await conn.execute(q, state, task_id)
