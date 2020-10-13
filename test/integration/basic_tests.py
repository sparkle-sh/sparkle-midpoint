import requests
from base import MidpointTestBase
from sparkle_test_base.config import MIDPOINT_API_BASE


class BasicTests(MidpointTestBase):
    def setUp(self):
        super().setUp()
        self.url = MIDPOINT_API_BASE

    def test_root_endpoint(self):
        code, res = self.wrapped_request(requests.get, self.url)
        self.assertEqual(code, 200)
        self.assertEqual(res.get("name"), "sparkle-midpoint")

        version = res.get("version")
        self.assertIsNotNone(version)
        self.assertIn('minor', version)
        self.assertIn('major', version)
        self.assertIn('build', version)
