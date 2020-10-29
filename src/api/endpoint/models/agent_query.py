# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from .base_model_ import Model
from . import util
from .agent import Agent


class AgentQuery(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, agent: Agent=None):  # noqa: E501
        """AgentQuery - a model defined in Swagger

        :param agent: The agent of this AgentQuery.  # noqa: E501
        :type agent: Agent
        """
        self.swagger_types = {
            'agent': Agent
        }

        self.attribute_map = {
            'agent': 'agent'
        }

        self._agent = agent

    @classmethod
    def from_dict(cls, dikt) -> 'AgentQuery':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The AgentQuery of this AgentQuery.  # noqa: E501
        :rtype: AgentQuery
        """
        return util.deserialize_model(dikt, cls)

    @property
    def agent(self) -> Agent:
        """Gets the agent of this AgentQuery.


        :return: The agent of this AgentQuery.
        :rtype: Agent
        """
        return self._agent

    @agent.setter
    def agent(self, agent: Agent):
        """Sets the agent of this AgentQuery.


        :param agent: The agent of this AgentQuery.
        :type agent: Agent
        """

        self._agent = agent