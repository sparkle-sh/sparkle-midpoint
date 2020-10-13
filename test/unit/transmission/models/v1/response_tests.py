import unittest
import ddt
from transmission.models.v1.res import *
from transmission.models.v1.res.response import Response
from transmission.models.v1.res.responses import *
from core.error import *


@ddt.ddt
class ResponseTests(unittest.TestCase):
    def test_when_creating_not_implemented_response_expect_throw(self):
        self.assertRaises(NotImplementedError, lambda: Response({}))

    TEST_CASES = [
        ("handshake_response", HandshakeResponse),
        ("ack_response", AckResponse),
        ("get_device_state_response", GetDeviceStateResponse),
        ("get_device_datasheet_response", GetDeviceDatasheetResponse),
        ("get_sensor_value_response", GetSensorValueResponse),
        ("list_devices_response", ListDevicesResponse)
    ]

    @ddt.data(*TEST_CASES)
    @ddt.unpack
    def test_when_getting_response_expect_correct_model(self, str_response, model_response):
        m = HEADER_TO_RESPONSE[str_response]
        self.assertEqual(m, model_response)


class AckResponseTests(unittest.TestCase):
    def test_when_creating_with_wrong_header_expect_throw(self):
        p = {"header": "fff"}
        self.assertRaises(ConnectorModelError, lambda: AckResponse(p))

    def test_when_creatig_with_valid_payload_expect_no_throw(self):
        p = {"header": "ack_response"}
        try:
            AckResponse(p)
        except Exception:
            self.fail()


class GetDeviceDatasheetResponseTests(unittest.TestCase):
    def test_when_creating_with_invalid_header_expect_throw(self):
        p = {"header": "ff"}
        self.assertRaises(ConnectorModelError,
                          lambda: GetDeviceDatasheetResponse(p))

    def test_when_creating_without_datasheet_in_content_expect_throw(self):
        p = {"header": "get_device_datasheet_response", "content": {}}
        self.assertRaises(ConnectorModelError,
                          lambda: GetDeviceDatasheetResponse(p))

    def test_when_creating_with_good_payload_expect_no_throw(self):
        ds = ['ab', 'cd']
        p = {
            "header": "get_device_datasheet_response",
            "content": {
                "datasheet": ds
            }
        }
        res = GetDeviceDatasheetResponse(p)
        self.assertEqual(res.get_datasheet(), ds)


class GetDeviceStateResponseTests(unittest.TestCase):
    def test_when_creating_with_wrong_header_expect_throw(self):
        p = {"header": "ff"}
        self.assertRaises(ConnectorModelError,
                          lambda: GetDeviceStateResponse(p))

    def test_when_creating_without_state_in_content_expect_throw(self):
        p = {"header": "get_device_state_response", "content": {}}
        self.assertRaises(ConnectorModelError,
                          lambda: GetDeviceStateResponse(p))

    def test_when_creating_with_good_payload_expect_no_throw(self):
        p = {"header": "get_device_state_response", "content": {"state": 123}}
        res = GetDeviceStateResponse(p)
        self.assertEqual(res.get_state(), 123)


class GetSensorValueResponseTests(unittest.TestCase):
    def test_when_creating_with_wrong_header_expect_throw(self):
        p = {"header": "ff"}
        self.assertRaises(ConnectorModelError,
                          lambda: GetSensorValueResponse(p))

    def test_when_creating_without_values_in_content_expect_throw(self):
        p = {"header": "get_sensor_value_response", "content": {}}
        self.assertRaises(ConnectorModelError,
                          lambda: GetSensorValueResponse(p))

    def test_when_creating_with_good_payload_expect_no_throw(self):
        values = {"a": 1, "b": 2}
        p = {"header": "get_sensor_value_response",
             "content": {"values": values}}
        res = GetSensorValueResponse(p)
        self.assertEqual(res.get_values(), values)


class HandshakeResponseTests(unittest.TestCase):
    def test_when_creating_with_wrong_header_expect_throw(self):
        p = {"header": "fff"}
        self.assertRaises(ConnectorModelError, lambda: HandshakeResponse(p))

    def test_when_creatig_with_valid_payload_expect_no_throw(self):
        p = {"header": "handshake_response"}
        try:
            HandshakeResponse(p)
        except Exception:
            self.fail()


class ListDevicesResponseTests(unittest.TestCase):
    def test_when_creating_with_wrong_header_expect_throw(self):
        p = {"header": "ff"}
        self.assertRaises(ConnectorModelError,
                          lambda: ListDevicesResponse(p))

    def test_when_creating_without_devices_in_content_expect_throw(self):
        p = {"header": "list_devices_response", "content": {}}
        self.assertRaises(ConnectorModelError,
                          lambda: ListDevicesResponse(p))

    def test_when_creating_with_good_payload_expect_no_throw(self):
        values = {"a": 1, "b": 2}
        p = {"header": "list_devices_response",
             "content": {"devices": values}}
        res = ListDevicesResponse(p)
        self.assertEqual(res.get_devices(), values)