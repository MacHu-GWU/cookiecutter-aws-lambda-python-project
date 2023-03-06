# -*- coding: utf-8 -*-

import typing as T
import os

import attr

from ..config.init import config
from ..boto_ses import bsm
from ..runtime import IS_LAMBDA


class StackDoesntExist(Exception):
    pass


@attr.s
class Output:
    """
    Output is an abstraction layer representing a CloudFormation stack output.
    It allows you to access the CloudFormation output values.
    """
    iam_role_lambda_arn: str = attr.ib()

    @classmethod
    def _get_from_stack(cls, env_name: str) -> "Output":
        """
        This function will only be called from local and CI, which depends on
        ``cottonformation`` library (about 24 MB uncompressed). In lambda function
        we load the information from env var. so we don't need ``cottonformation``.
        """
        from .define import Stack

        stack = Stack(env=config.get_env(env_name))

        try:
            return cls(
                iam_role_lambda_arn=stack.get_output_value(
                    bsm, stack.output_iam_role_lambda_arn.id
                ),
            )
        except Exception as e:
            if "does not exist" in str(e):
                raise StackDoesntExist

    @classmethod
    def _get_from_env_var(cls) -> "Output":
        """
        This will only be used in computational runtime,
        for example: ec2, lambda, ecs.
        """
        return cls(
            iam_role_lambda_arn="",
        )

    @classmethod
    def get(cls, env_name: T.Optional[str] = None) -> "Output":
        if IS_LAMBDA:
            return cls._get_from_env_var()
        else:
            if env_name is None:
                env_name = config.get_current_env()
            return cls._get_from_stack(env_name)
