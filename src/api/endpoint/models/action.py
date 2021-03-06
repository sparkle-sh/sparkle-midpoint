# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from .base_model_ import Model
from . import util


class Action(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, name: str = None, device_id: int = None):  # noqa: E501
        """Action - a model defined in Swagger

        :param name: The name of this Action.  # noqa: E501
        :type name: str
        :param device_id: The device_id of this Action.  # noqa: E501
        :type device_id: int
        """
        self.swagger_types = {
            'name': str,
            'device_id': int
        }

        self.attribute_map = {
            'name': 'name',
            'device_id': 'device_id'
        }

        self._name = name
        self._device_id = device_id

    @classmethod
    def from_dict(cls, dikt) -> 'Action':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Action of this Action.  # noqa: E501
        :rtype: Action
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Action.


        :return: The name of this Action.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Action.


        :param name: The name of this Action.
        :type name: str
        """

        self._name = name

    @property
    def device_id(self) -> int:
        """Gets the device_id of this Action.


        :return: The device_id of this Action.
        :rtype: int
        """
        return self._device_id

    @device_id.setter
    def device_id(self, device_id: int):
        """Sets the device_id of this Action.


        :param device_id: The device_id of this Action.
        :type device_id: int
        """

        self._device_id = device_id
