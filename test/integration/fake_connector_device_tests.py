import requests
from fake_connector_base import FakeConnectorTestsBase
from sparkle_test_base.fakes.config import *


class FakeConnectorDeviceTests(FakeConnectorTestsBase):
    handshake = {
        "header": "handshake_response",
        "content": {}
    }

    ack = {
        "header": "ack_response",
        "content": {}
    }

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

    def test_switch_device_state_without_device_id(self):
        payload = {
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
        self.assertEqual(code, 400)

    def test_switch_device_state_without_state(self):
        payload = {
            "device_id": 0,
            "agent": {
                "id": self.agent_id,
            },
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

    #TO DO
    # def test_get_sensor_value(self):
    #     labels = ["temperature"]

    #     payload = {
    #         "agent_id": self.agent_id,
    #         "device_id": 0,
    #         "labels": labels
    #     }

    #     values = {
    #         "values": {
    #             "temperature": 123.5
    #         }
    #     }

    #     response = {
    #         "header": "get_sensor_value_response",
    #         "content": {
    #             "values": values
    #         }
    #     }

    #     self.fake_connector.enqueue_response(response)

    #     url = "{}/device/value".format(MIDPOINT_API_BASE)
    #     code, content = self.wrapped_request(requests.get, url, json=payload)
    #     self.assertEqual(code, 200)

    #     self.assertEqual(content.get("values"), values)
   
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