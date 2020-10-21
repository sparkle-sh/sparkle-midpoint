import unittest
from transmission.models.v1.req import *
from transmission.models.v1.req.request import Request


class RequestTests(unittest.TestCase):
    def test_when_serializing_not_implemented_method_expect_throw(self):
        req = Request()
        self.assertRaises(NotImplementedError, req.serialize)

class DisconnectRequestTests(unittest.TestCase):
    def test_when_serializing_except_correct_result(self):
        req = DisconnectRequest()
        serialized = req.serialize()

        payload = {
            "header": "disconnect_request",
            "content": {
            }
        }
        self.assertEqual(payload, serialized)

class GetDeviceDatasheetRequestTests(unittest.TestCase):
    def test_when_serializing_except_correct_result(self):
        device_id = 1
        req = GetDeviceDatasheetRequest(device_id)
        serialized = req.serialize()
        payload = {
            "header": "get_device_datasheet_request",
            "content": {
                "device_id": device_id
            }
        }
        self.assertEqual(payload, serialized)

class GetDeviceStateRequestTests(unittest.TestCase):
    def test_when_serializing_except_correct_result(self):
        device_id = 1
        req = GetDeviceStateRequest(device_id)
        serialized = req.serialize()
        payload = {
            "header": "get_device_state_request",
            "content": {
                "device_id": device_id
            }
        }
        self.assertEqual(payload, serialized)

class GetSensorValueRequestTests(unittest.TestCase):
    def test_when_serializing_except_correct_result(self):
        device_id = 1
        labels = { "label1", "label2"}
        req = GetSensorValueRequest(device_id, labels)
        serialized = req.serialize()
        payload = {
            "header": "get_device_state_request",
            "content": {
                "device_id": device_id,
                "labels": labels
            }
        }
        self.assertEqual(payload, serialized)

class HandshakeRequestTests(unittest.TestCase):
    def test_when_serializing_except_correct_result(self):
        req = HandshakeRequest()
        serialized = req.serialize()
        payload = {
            "header": "handshake_request",
            "content": {
                "session_type": "agent"
            }
        }
        self.assertEqual(payload, serialized)

class ListDevicesRequestTests(unittest.TestCase):
    def test_when_serializing_except_correct_result(self):
        req = ListDevicesRequest()
        serialized = req.serialize()
        payload = {
            "header": "list_devices_request",
            "content": {}
        }
        self.assertEqual(payload, serialized)

class SwitchDeviceStateRequestTeste(unittest.TestCase):
    def test_when_serializing_except_correct_result(self):
        device_id = 1
        state = 1
        req = SwitchDeviceStateRequest(device_id, state)
        serialized = req.serialize()
        payload = {
            "header": "switch_device_state_request",
            "content": {
                "device_id": device_id,
                "state": state
            }
        }
        self.assertEqual(payload, serialized)