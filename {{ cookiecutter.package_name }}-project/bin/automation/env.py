# -*- coding: utf-8 -*-

"""
**Environment Definition**

Environment is basically a group of resources with specific name space.

This module automatically detect what environment we should use.
"""

import os
import json

from {{ cookiecutter.package_name }}.config.define import EnvEnum

from .git import (
    GIT_BRANCH_NAME,
    IS_MASTER_BRANCH,
    IS_FEATURE_BRANCH,
    IS_INT_BRANCH,
    IS_RELEASE_BRANCH,
    IS_CLEAN_UP_BRANCH,
    # on clean up branch, you have to explicitly define which env you want to clean up
    IS_CF_BRANCH,
    IS_LAYER_BRANCH,
    IS_LAMBDA_BRANCH,
    IS_ECR_BRANCH,
)
from .runtime import IS_CI
from .paths import path_current_env_name_json
from .logger import logger


def _find_env() -> str:
    """
    Find which environment we should deploy to.
    """
    if IS_CI:
        if (
            IS_FEATURE_BRANCH
            or IS_CF_BRANCH
            or IS_LAYER_BRANCH
            or IS_LAMBDA_BRANCH
            or IS_ECR_BRANCH
        ):
            return EnvEnum.dev.value
        elif IS_INT_BRANCH:
            return EnvEnum.int.value
        elif IS_RELEASE_BRANCH:
            return EnvEnum.prod.value
        elif IS_CLEAN_UP_BRANCH:
            parts = GIT_BRANCH_NAME.lower().split("/") # e.g. "cleanup/${env_name}/..."
            if len(parts) == 1:
                raise ValueError(
                    f"Invalid cleanup branch name {GIT_BRANCH_NAME!r}! "
                    "Your branch name should be 'cleanup/${env_name}/...'."
                )
            env_name = parts[1]
            if env_name not in EnvEnum._value2member_map_:
                raise ValueError(
                    f"Invalid environment name {env_name!r}! "
                    "Your branch name should be 'cleanup/${env_name}/...'."
                )
            return env_name
        else:
            raise NotImplementedError
    # if it is not in CI (on local laptop), it is always deploy to dev
    else:
        # you can uncomment this line to force to use certain env
        # from your local laptop to run automation, deployment script ...
        # return EnvEnum.dev.value
        return EnvEnum.dev.value


def find_env() -> str:
    # find which environment we should deploy to.
    env_name = _find_env()
    # write the env to cache for application code to use
    path_current_env_name_json.write_text(
        json.dumps(
            {
                "env": env_name,
                "description": "DON'T edit this file manually!",
            },
            indent=4,
        )
    )
    return env_name


CURRENT_ENV = find_env()


def print_env_info():
    logger.info(f"Current environment name is 🏢 {CURRENT_ENV!r}")
