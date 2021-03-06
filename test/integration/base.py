from sparkle_test_base.base import TestBase
from sparkle_test_base.config import MIDPOINT_API_BASE


class MidpointTestBase(TestBase):
    def setUp(self):
        super().setUp()
        self.url = MIDPOINT_API_BASE
        if self.is_test_env():
            self.start_database(local=True)
            self.wait_for_database()

            self.start_midpoint(local=True, with_cov=True, save_logs=True)
            self.wait_for_midpoint()
