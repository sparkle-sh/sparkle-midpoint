# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class SwitchableDeviceDatasheetDatasheet(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, values: List[int]=None):  # noqa: E501
        """SwitchableDeviceDatasheetDatasheet - a model defined in Swagger

        :param values: The values of this SwitchableDeviceDatasheetDatasheet.  # noqa: E501
        :type values: List[int]
        """
        self.swagger_types = {
            'values': List[int]
        }

        self.attribute_map = {
            'values': 'values'
        }

        self._values = values

    @classmethod
    def from_dict(cls, dikt) -> 'SwitchableDeviceDatasheetDatasheet':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SwitchableDeviceDatasheet_datasheet of this SwitchableDeviceDatasheetDatasheet.  # noqa: E501
        :rtype: SwitchableDeviceDatasheetDatasheet
        """
        return util.deserialize_model(dikt, cls)

    @property
    def values(self) -> List[int]:
        """Gets the values of this SwitchableDeviceDatasheetDatasheet.


        :return: The values of this SwitchableDeviceDatasheetDatasheet.
        :rtype: List[int]
        """
        return self._values

    @values.setter
    def values(self, values: List[int]):
        """Sets the values of this SwitchableDeviceDatasheetDatasheet.


        :param values: The values of this SwitchableDeviceDatasheetDatasheet.
        :type values: List[int]
        """

        self._values = values
