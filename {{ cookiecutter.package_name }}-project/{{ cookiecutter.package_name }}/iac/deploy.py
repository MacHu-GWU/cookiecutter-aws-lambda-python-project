# -*- coding: utf-8 -*-

"""
This module implements the automation to deploy CloudFormation stack.
"""

import cottonformation as cf

from ..boto_ses import bsm
from ..config.init import config

from .define import Stack


def deploy_cloudformation_stack(env_name: str) -> str:
    env = config.get_env(env_name)

    tpl = cf.Template(Description="Application - Documentation Storage")

    stack = Stack(env=env)

    tpl.add(stack.rg1_iam)

    tpl.batch_tagging(
        tags=dict(
            ProjectName=env.project_name,
            EnvName=env.env_name,
        ),
        mode_overwrite=True,
    )

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


def delete_cloudformation_stack(env_name: str) -> str:
    env = config.get_env(env_name)
    stack = Stack(env=env)
    cf_env = cf.Env(bsm=bsm)
    cf_env.delete(stack_name=stack.stack_name, timeout=120)
    return stack.stack_name
