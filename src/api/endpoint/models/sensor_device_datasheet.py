# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from .base_model_ import Model
from . import util


class SensorDeviceDatasheet(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, datasheet: SensorDeviceDatasheetDatasheet=None):  # noqa: E501
        """SensorDeviceDatasheet - a model defined in Swagger

        :param datasheet: The datasheet of this SensorDeviceDatasheet.  # noqa: E501
        :type datasheet: SensorDeviceDatasheetDatasheet
        """
        self.swagger_types = {
            'datasheet': SensorDeviceDatasheetDatasheet
        }

        self.attribute_map = {
            'datasheet': 'datasheet'
        }

        self._datasheet = datasheet

    @classmethod
    def from_dict(cls, dikt) -> 'SensorDeviceDatasheet':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SensorDeviceDatasheet of this SensorDeviceDatasheet.  # noqa: E501
        :rtype: SensorDeviceDatasheet
        """
        return util.deserialize_model(dikt, cls)

    @property
    def datasheet(self) -> SensorDeviceDatasheetDatasheet:
        """Gets the datasheet of this SensorDeviceDatasheet.


        :return: The datasheet of this SensorDeviceDatasheet.
        :rtype: SensorDeviceDatasheetDatasheet
        """
        return self._datasheet

    @datasheet.setter
    def datasheet(self, datasheet: SensorDeviceDatasheetDatasheet):
        """Sets the datasheet of this SensorDeviceDatasheet.


        :param datasheet: The datasheet of this SensorDeviceDatasheet.
        :type datasheet: SensorDeviceDatasheetDatasheet
        """

        self._datasheet = datasheet
