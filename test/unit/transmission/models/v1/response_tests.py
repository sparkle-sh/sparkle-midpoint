import unittest
import ddt
from transmission.models.v1.res import *
from transmission.models.v1.res.response import Response
from transmission.models.v1.res.responses import *
from transmission.models.v1.device_type import DeviceType
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
        ("get_sensor_value_response", GetDeviceValueResponse),
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

    def test_when_creating_with_states_expect_switchable(self):
        ds = [1, 0]
        p = {
            "header": "get_device_datasheet_response",
            "content": {
                "datasheet": {"states": ds}
            }
        }
        res = GetDeviceDatasheetResponse(p)
        self.assertEqual(res.get_device_type(), DeviceType.SWITCHABLE)

    def test_when_creating_with_labels_expect_sensor(self):
        ds = ['ab', 'cd']
        p = {
            "header": "get_device_datasheet_response",
            "content": {
                "datasheet": {"labels": ds}
            }
        }
        res = GetDeviceDatasheetResponse(p)
        self.assertEqual(res.get_device_type(), DeviceType.SENSOR)


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
        p = {"header": "get_device_state_response",
             "content": {"state": {"state_value": 123}}}
        res = GetDeviceStateResponse(p)
        self.assertEqual(res.get_state().get("state_value"), 123)


class GetDeviceValueResponseTests(unittest.TestCase):
    def test_when_creating_with_wrong_header_expect_throw(self):
        p = {"header": "ff"}
        self.assertRaises(ConnectorModelError,
                          lambda: GetDeviceValueResponse(p))

    def test_when_creating_without_values_in_content_expect_throw(self):
        p = {"header": "get_sensor_value_response", "content": {}}
        self.assertRaises(ConnectorModelError,
                          lambda: GetDeviceValueResponse(p))

    def test_when_creating_with_good_payload_expect_no_throw(self):
        values = {"a": 1, "b": 2}
        p = {"header": "get_sensor_value_response",
             "content": {"values": values}}
        res = GetDeviceValueResponse(p)
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
