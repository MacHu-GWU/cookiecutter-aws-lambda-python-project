# -*- coding: utf-8 -*-

"""
This module is the CloudFormation stack definition.
"""

import typing as T
import copy

import attr
import cottonformation as cf

from ...config.define.main import Env

from .iam import IamMixin


@attr.s
class Stack(
    cf.Stack,
    IamMixin,
):
    """
    A Python class wrapper around the real CloudFormation stack, to provide
    attribute access to different AWS Resources.

    :param env: the ``Env`` object in config definition. it is used to derive
        a lot of value for AWS resources.
    """

    env: T.Optional[Env] = attr.ib(default=None)

    @property
    def stack_name(self) -> str:
        return self.env.prefix_name_slug

    def encode_policy_document(self, statement: T.List[dict]) -> dict:
        policy_document = {
            "Version": "2012-10-17",
        }
        new_statement = list()
        for ith, stat in enumerate(statement, start=1):
            new_stat = copy.deepcopy(stat)
            new_stat["Sid"] = f"Sid{str(ith).zfill(3)}"
            new_statement.append(new_stat)

        policy_document["Statement"] = new_statement
        return policy_document

    def post_hook(self):
        self.mk_rg1_iam()

