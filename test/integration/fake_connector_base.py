import os
from base import MidpointTestBase
from sparkle_test_base.fakes import FakeConnector


class FakeConnectorTestsBase(MidpointTestBase):
    def setUp(self):
        super().setUp()
        self.fake_connector = FakeConnector()
        self.fake_connector.start()

    def tearDown(self):
        super().tearDown()
        self.fake_connector.stop()
