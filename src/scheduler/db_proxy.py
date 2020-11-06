from src.core.db import ConnectionPool
from src.scheduler.task.task import TaskType


class DatabaseProxy(object):
    async def insert_task(self, task, uuid):
        task_type = task.get_type()

        q = "INSERT INTO {}_tasks (task_id, device_id, action, {}) VALUES (%s, %s, %s, %s)"
        type_string, time_table = (
            'periodic', 'interval') if task_type == TaskType.Periodic else ('deferred', 'delay')
        action = task.action.serialize().get('name')

        async with ConnectionPool.acquire_connection() as conn:
            await conn.query(q.format(type_string, time_table,
                                      (uuid, task.device_id, action, getattr(task, time_table))))

    async def delete_task(self, task_type, task_id):
        table = 'periodic' if task_type == TaskType.Periodic else 'deferred'
        q = f"DELETE FROM {table}_tasks WHERE task_id=%s"

        async with ConnectionPool.acquire_connection as conn:
            await conn.query(q, (task_id,))
