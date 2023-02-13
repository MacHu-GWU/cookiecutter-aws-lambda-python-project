# -*- coding: utf-8 -*-

"""
This module is the CloudFormation stack definition.
"""

import typing as T
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

    def encode_statement(self, statement: T.List[dict]) -> T.List[dict]:
        for ith, stat in enumerate(statement, start=1):
            stat["Sid"] = f"Sid{str(ith).zfill(3)}"
        return statement

    def post_hook(self):
        self.mk_rg1_iam()
