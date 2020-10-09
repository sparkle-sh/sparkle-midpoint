from sparkle_test_base.base import TestBase


class MidpointTestBase(TestBase):
    def setUp(self):
        super().setUp()
        if self.is_test_env():
            self.start_midpoint()
            self.wait_for_midpoint()
    
