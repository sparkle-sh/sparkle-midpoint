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

    def test_invalid_route(self):
        code, res = self.wrapped_request(requests.get, f'{self.url}/ala_ma_kota')
        self.assertEqual(code, 404)
        self.assertEqual(res.get("code"), 400)

    def test_method_not_allowed(self):
        code, res = self.wrapped_request(requests.post, self.url)
        self.assertEqual(code, 405)
        self.assertEqual(res.get("code"), 400)

    def test_connect_with_connector_down(self):
        code, res = self.wrapped_request(requests.post, f'{self.url}/agent')
        self.assertEqual(code, 400)
        self.assertIn('connector is down', res['description'])

    def test_disconnect_without_body(self):
        code, res = self.wrapped_request(requests.delete, f'{self.url}/agent')
        self.assertEqual(code, 400)
        self.assertIn('empty', res['description'])

    def test_disconnect_with_invalid_key(self):
        payload = {'hello': 'world'}
        code, res = self.wrapped_request(
            requests.delete, f'{self.url}/agent', json=payload)
        self.assertEqual(code, 400)
        self.assertIn('corrupted', res['description'])

    def test_disconnect_with_invalid_agent_id(self):
        payload = {'id': 'world'}
        code, res = self.wrapped_request(
            requests.delete, f'{self.url}/agent', json=payload)
        self.assertEqual(code, 400)
        self.assertIn('not exist', res['description'])
