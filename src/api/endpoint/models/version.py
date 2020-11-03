# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Version(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, major: int=None, minor: int=None, build: int=None):  # noqa: E501
        """Version - a model defined in Swagger

        :param major: The major of this Version.  # noqa: E501
        :type major: int
        :param minor: The minor of this Version.  # noqa: E501
        :type minor: int
        :param build: The build of this Version.  # noqa: E501
        :type build: int
        """
        self.swagger_types = {
            'major': int,
            'minor': int,
            'build': int
        }

        self.attribute_map = {
            'major': 'major',
            'minor': 'minor',
            'build': 'build'
        }

        self._major = major
        self._minor = minor
        self._build = build

    @classmethod
    def from_dict(cls, dikt) -> 'Version':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Version of this Version.  # noqa: E501
        :rtype: Version
        """
        return util.deserialize_model(dikt, cls)

    @property
    def major(self) -> int:
        """Gets the major of this Version.


        :return: The major of this Version.
        :rtype: int
        """
        return self._major

    @major.setter
    def major(self, major: int):
        """Sets the major of this Version.


        :param major: The major of this Version.
        :type major: int
        """
        if major is None:
            raise ValueError("Invalid value for `major`, must not be `None`")  # noqa: E501

        self._major = major

    @property
    def minor(self) -> int:
        """Gets the minor of this Version.


        :return: The minor of this Version.
        :rtype: int
        """
        return self._minor

    @minor.setter
    def minor(self, minor: int):
        """Sets the minor of this Version.


        :param minor: The minor of this Version.
        :type minor: int
        """
        if minor is None:
            raise ValueError("Invalid value for `minor`, must not be `None`")  # noqa: E501

        self._minor = minor

    @property
    def build(self) -> int:
        """Gets the build of this Version.


        :return: The build of this Version.
        :rtype: int
        """
        return self._build

    @build.setter
    def build(self, build: int):
        """Sets the build of this Version.


        :param build: The build of this Version.
        :type build: int
        """
        if build is None:
            raise ValueError("Invalid value for `build`, must not be `None`")  # noqa: E501

        self._build = build
