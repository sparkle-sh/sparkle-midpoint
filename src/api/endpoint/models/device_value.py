# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from .base_model_ import Model
from . import util


class DeviceValue(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, value: int = None):  # noqa: E501
        """DeviceValue - a model defined in Swagger

        :param value: The value of this DeviceValue.  # noqa: E501
        :type value: int
        """
        self.swagger_types = {
            'value': int
        }

        self.attribute_map = {
            'value': 'value'
        }

        self._value = value

    @classmethod
    def from_dict(cls, dikt) -> 'DeviceValue':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DeviceValue of this DeviceValue.  # noqa: E501
        :rtype: DeviceValue
        """
        return util.deserialize_model(dikt, cls)

    @property
    def value(self) -> int:
        """Gets the value of this DeviceValue.


        :return: The value of this DeviceValue.
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value: int):
        """Sets the value of this DeviceValue.


        :param value: The value of this DeviceValue.
        :type value: int
        """

        self._value = value
