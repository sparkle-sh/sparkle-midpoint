# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from .base_model_ import Model
from . import util
from .device import Device


class Devices(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, devices: List[Device] = None):  # noqa: E501
        """Devices - a model defined in Swagger

        :param devices: The devices of this Devices.  # noqa: E501
        :type devices: List[Device]
        """
        self.swagger_types = {
            'devices': List[Device]
        }

        self.attribute_map = {
            'devices': 'devices'
        }

        self._devices = devices

    @classmethod
    def from_dict(cls, dikt) -> 'Devices':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Devices of this Devices.  # noqa: E501
        :rtype: Devices
        """
        return util.deserialize_model(dikt, cls)

    @property
    def devices(self) -> List[Device]:
        """Gets the devices of this Devices.


        :return: The devices of this Devices.
        :rtype: List[Device]
        """
        return self._devices

    @devices.setter
    def devices(self, devices: List[Device]):
        """Sets the devices of this Devices.


        :param devices: The devices of this Devices.
        :type devices: List[Device]
        """

        self._devices = devices
