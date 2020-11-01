import asynctest
from src.scheduler.task.task import *


class TaskTests(asynctest.TestCase):
    async def test_when_update_on_base_task_expect_exception(self):
        t = Task(None, None, None)
        try:
            await t.update()
        except NotImplementedError:
            return
        self.fail(msg="Update did not throw")
