# -*- coding: utf-8 -*-

"""
This module implements the automation to deploy CloudFormation stack.
"""

import typing as T

import cottonformation as cf
from aws_cloudformation.better_boto import describe_live_stack

from .._version import __version__
from ..boto_ses import bsm
from ..config.init import config
from ..runtime import IS_CI

from .define import Stack


def deploy_cloudformation_stack(
    env_name: str,
    dry_run: bool = True,
) -> str:
    """
    Deploy (Create / Update) CloudFormation Stack using ChangeSet.

    :return: the name of stack been deployed.
    """
    env = config.get_env(env_name)

    tpl = cf.Template(Description="Application - Documentation Storage")

    stack = Stack(env=env)

    tpl.add(stack.rg1_iam)

    tpl.batch_tagging(
        tags=dict(
            ProjectName=env.project_name,
            EnvName=env.env_name,
            PackageVersion=__version__,
        ),
        mode_overwrite=True,
    )

    if dry_run is False:
        cf_env = cf.Env(bsm=bsm)

        cf_env.deploy(
            stack_name=stack.stack_name,
            template=tpl,
            tags=dict(
                ProjectName=env.project_name,
                EnvName=env.env_name,
            ),
            bucket=config.env.s3dir_artifacts.bucket,
            prefix=config.env.s3dir_cloudformation_templates.key,
            include_named_iam=True,
            skip_prompt=True,
            timeout=120,
            change_set_timeout=120,
        )

    return stack.stack_name


def delete_cloudformation_stack(env_name: str) -> T.Optional[str]:
    """
    Delete CloudFormation Stack if exists.

    :return: the name of stack been deleted, return None if stack doesn't exists
    """
    env = config.get_env(env_name)
    stack = Stack(env=env)

    if describe_live_stack(bsm, name=stack.stack_name) is None:
        return None

    cf_env = cf.Env(bsm=bsm)
    kwargs = dict(
        stack_name=stack.stack_name,
        timeout=120,
    )
    if IS_CI:
        kwargs["skip_prompt"] = True
    cf_env.delete(**kwargs)
    return stack.stack_name
