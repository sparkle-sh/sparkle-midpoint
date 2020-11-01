import requests
import ddt
from fake_connector_base import FakeConnectorTestsBase
from sparkle_test_base.fakes.config import *


@ddt.ddt
class FakeConnectorDeviceTests(FakeConnectorTestsBase):
    handshake = {
        "header": "handshake_response",
        "content": {}
    }

    ack = {
        "header": "ack_response",
        "content": {}
    }

    AGENT_TEST_CASES = [
        ("/", {}, "get"),
        ("/state", {"device_id": 0}, "get"),
        ("/state", {"device_id": 0, "state": {"state_value": 1}}, "put"),
        ("/datasheet", {"device_id": 0}, "get"),
        ("/value", {"device_id": 0, "labels": ["temperature"]}, "get")
    ]

    AGENT_ID_TEST_CASES = [
        ("/", {"agent": {}}, "get"),
        ("/state", {"device_id": 0, "agent": {}}, "get"),
        ("/state", {"device_id": 0, "agent": {},
                    "state": {"state_value": 1}}, "put"),
        ("/datasheet", {"device_id": 0, "agent": {}}, "get"),
        ("/value", {"device_id": 0, "agent": {},
                    "labels": ["temperature"]}, "get")
    ]

    DEVICE_ID_TEST_CASES = [
        ("/state", {}, "get"),
        ("/state", {
            "state": {"state_value": 1}}, "put"),
        ("/datasheet", {}, "get"),
        ("/value", {
            "labels": ["temperature"]}, "get")
    ]

    def setUp(self):
        super().setUp()
        self.fake_connector.enqueue_response(self.handshake)

        url = "{}/agent".format(MIDPOINT_API_BASE)
        code, payload = self.wrapped_request(requests.post, url)
        self.assertEqual(code, 201)
        self.agent_id = payload.get("id")

    def tearDown(self):
        self.fake_connector.enqueue_response(self.ack)
        url = "{}/agent".format(MIDPOINT_API_BASE)
        code, _ = self.wrapped_request(requests.delete, url, json={
                                       "id": self.agent_id})
        self.assertEqual(code, 200)
        super().tearDown()

    def test_connect_disconnect(self):
        pass

    @ddt.data(*AGENT_TEST_CASES)
    @ddt.unpack
    def test_device_endpoints_without_agent(self, endpoint, req_payload, method):
        payload = req_payload
        self.fake_connector.enqueue_response(self.ack)
        url = "{}/device{}".format(MIDPOINT_API_BASE, endpoint)
        if method == "get":
            code, _ = self.wrapped_request(requests.get, url, json=payload)
        if method == "put":
            code, _ = self.wrapped_request(requests.put, url, json=payload)
        self.assertEqual(code, 400)

    @ddt.data(*AGENT_ID_TEST_CASES)
    @ddt.unpack
    def test_device_endpoints_without_agent_id(self, endpoint, req_payload, method):
        payload = req_payload
        self.fake_connector.enqueue_response(self.ack)
        url = "{}/device{}".format(MIDPOINT_API_BASE, endpoint)
        if method == "get":
            code, _ = self.wrapped_request(requests.get, url, json=payload)
        if method == "put":
            code, _ = self.wrapped_request(requests.put, url, json=payload)
        self.assertEqual(code, 400)

    @ddt.data(*DEVICE_ID_TEST_CASES)
    @ddt.unpack
    def test_device_endpoints_without_device_id(self, endpoint, req_payload, method):
        payload = req_payload
        payload["agent"] = self.agent_id
        self.fake_connector.enqueue_response(self.ack)
        url = "{}/device{}".format(MIDPOINT_API_BASE, endpoint)
        if method == "get":
            code, _ = self.wrapped_request(requests.get, url, json=payload)
        if method == "put":
            code, _ = self.wrapped_request(requests.put, url, json=payload)
        self.assertEqual(code, 400)

    def test_switch_device_state(self):
        payload = {
            "device_id": 0,
            "agent": {
                "id": self.agent_id,
            },
            "state": {
                "state_value": 1
            }
        }

        self.fake_connector.enqueue_response(self.ack)
        url = "{}/device/state".format(MIDPOINT_API_BASE)
        code, _ = self.wrapped_request(requests.put, url, json=payload)
        self.assertEqual(code, 200)

    def test_switch_device_state_without_state(self):
        payload = {
            "device_id": 0,
            "agent": {
                "id": self.agent_id,
            }
        }

        self.fake_connector.enqueue_response(self.ack)
        url = "{}/device/state".format(MIDPOINT_API_BASE)
        code, content = self.wrapped_request(requests.put, url, json=payload)
        self.assertEqual(code, 400)

    def test_get_device_state(self):
        payload = {
            "device_id": 0,
            "agent": {
                "id": self.agent_id
            }
        }

        state_value = 1

        response = {
            "header": "get_device_state_response",
            "content": {
                "state": {
                    "state_value": state_value
                }
            }
        }

        self.fake_connector.enqueue_response(response)

        url = "{}/device/state".format(MIDPOINT_API_BASE)
        code, content = self.wrapped_request(requests.get, url, json=payload)
        self.assertEqual(code, 200)
        self.assertEqual(content.get("state_value"), state_value)

    def test_get_sensor_device_datasheet(self):
        payload = {
            "device_id": 0,
            "agent": {
                "id": self.agent_id
            }
        }

        datasheet = {
            "labels": ["label1", "label2"]
        }

        response = {
            "header": "get_device_datasheet_response",
            "content": {
                "datasheet": datasheet
            }
        }

        self.fake_connector.enqueue_response(response)

        url = "{}/device/datasheet".format(MIDPOINT_API_BASE)
        code, content = self.wrapped_request(requests.get, url, json=payload)
        self.assertEqual(code, 200)
        self.assertEqual(content.get("datasheet"), datasheet)

    def test_get_switchable_device_datasheet(self):
        payload = {
            "device_id": 0,
            "agent": {
                "id": self.agent_id
            }
        }

        datasheet = {
            "values": [0, 1, 2]
        }

        response = {
            "header": "get_device_datasheet_response",
            "content": {
                "datasheet": datasheet
            }
        }

        self.fake_connector.enqueue_response(response)

        url = "{}/device/datasheet".format(MIDPOINT_API_BASE)
        code, content = self.wrapped_request(requests.get, url, json=payload)

        self.assertEqual(code, 200)
        self.assertEqual(content.get("datasheet"), datasheet)

    def test_list_devices(self):
        payload = {
            "agent": {
                "id": self.agent_id
            }
        }

        devices = [{
            "id": 0,
            "type": 0,
            "name": "device1",
            "description": "first device"
        }]
        response = {
            "header": "list_devices_response",
            "content": {
                "devices": devices
            }
        }

        self.fake_connector.enqueue_response(response)
        url = "{}/device".format(MIDPOINT_API_BASE)

        code, content = self.wrapped_request(
            requests.get, url, json=payload)
        self.assertEqual(code, 200)
        self.assertEqual(content.get("devices"), devices)

    def test_get_device_value(self):
        labels = ["temperature"]

        payload = {
            "device_id": 0,
            "agent": {
                "id": self.agent_id
            },
            "labels": labels
        }

        values = {
            "temperature": 123.5
        }

        response = {
            "header": "get_sensor_value_response",
            "content": {
                "values": values
            }
        }

        self.fake_connector.enqueue_response(response)

        url = "{}/device/value".format(MIDPOINT_API_BASE)
        code, content = self.wrapped_request(requests.get, url, json=payload)
        self.assertEqual(code, 200)
        self.assertEqual(content.get("values"), values)

    def test_get_device_value_without_labels(self):
        payload = {
            "device_id": 0,
            "agent": {
                "id": self.agent_id
            }
        }

        self.fake_connector.enqueue_response(self.ack)
        url = "{}/device/value".format(MIDPOINT_API_BASE)
        code, _ = self.wrapped_request(requests.get, url, json=payload)
        self.assertEqual(code, 400)

    # TO DO
    # def test_connector_request_failure_response(self):
    #     payload = {
    #         "device_id": 1,
    #         "agent": {
    #             "id": self.agent_id
    #         },
    #         "state": {
    #             "state_value": 1
    #         }
    #     }

    #     error, reason = 105, "reason"

    #     response = {
    #         "header": "request_failure_response",
    #         "content": {
    #             "error_code": error,
    #             "reason": reason
    #         }
    #     }

    #     self.fake_connector.enqueue_response(response)
    #     url = "{}/device/state".format(MIDPOINT_API_BASE)
    #     code, content = self.wrapped_request(requests.put, url, json=payload)
    #     self.assertEqual(code, 400)
    #     self.assertEqual(content.get("error_code"), error)
    #     self.assertEqual(content.get("description"), reason)
    #     self.assertEqual(content.get("connection_dropped"), False)

    # def test_connector_error_response(self):
    #     payload = {
    #         "device_id": 1,
    #         "agent": {
    #             "id": self.agent_id
    #         },
    #         "state": {
    #             "state_value": 1
    #         }
    #     }

    #     error, reason = 105, "reason"

    #     response = {
    #         "header": "error_response",
    #         "content": {
    #             "error_code": error,
    #             "error_details": reason
    #         }
    #     }

    #     self.fake_connector.enqueue_response(response)
    #     url = "{}/device/state".format(MIDPOINT_API_BASE)
    #     code, content = self.wrapped_request(requests.put, url, json=payload)
    #     self.assertEqual(code, 400)
    #     self.assertEqual(content.get("error_code"), error)
    #     self.assertEqual(content.get("description"), reason)
    #     self.assertEqual(content.get("connection_dropped"), True)
