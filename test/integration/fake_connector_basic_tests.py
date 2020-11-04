import requests
from fake_connector_base import FakeConnectorTestsBase
from sparkle_test_base.fakes.config import *


class FakeConnectorBasicTests(FakeConnectorTestsBase):
    def test_start_stop_fake_connector(self):
        pass

    def test_connect_agent(self):
        handshake = {
            "header": "handshake_response",
            "content": {}
        }

        ack = {
            "header": "ack_response",
            "content": {}
        }

        self.fake_connector.enqueue_response(handshake)
        self.fake_connector.enqueue_response(ack)

        url = "{}/agent".format(MIDPOINT_API_BASE)
        code, payload = self.wrapped_request(requests.post, url)

        self.assertEqual(code, 201)

    def test_disconnect_agent_with_invalid_agent_id(self):
        url = "{}/agent".format(MIDPOINT_API_BASE)
        code, payload = self.wrapped_request(
            requests.delete, url, headers={"Agent-ID": "1111"})
        self.assertEqual(code, 400)

    def test_disconnect_agent_without_agent_id(self):
        url = "{}/agent".format(MIDPOINT_API_BASE)
        code, payload = self.wrapped_request(
            requests.delete, url, headers={})
        self.assertEqual(code, 400)

    def test_disconnect_agent_with_empty_headers(self):
        url = "{}/agent".format(MIDPOINT_API_BASE)
        code, payload = self.wrapped_request(
            requests.delete, url)
        self.assertEqual(code, 400)

    def test_disconnect_agent_good(self):
        handshake = {
            "header": "handshake_response",
            "content": {}
        }

        ack = {
            "header": "ack_response",
            "content": {}
        }

        self.fake_connector.enqueue_response(handshake)
        self.fake_connector.enqueue_response(ack)
        self.fake_connector.enqueue_response(ack)

        url = "{}/agent".format(MIDPOINT_API_BASE)
        code, payload = self.wrapped_request(requests.post, url)
        self.assertEqual(code, 201)

        url = "{}/agent".format(MIDPOINT_API_BASE)
        code, payload = self.wrapped_request(
            requests.delete, url, headers={"Agent-ID": payload.get("id")})
        self.assertEqual(code, 200)
