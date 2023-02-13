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
    IS_MASTER_BRANCH,
    IS_FEATURE_BRANCH,
    IS_RELEASE_BRANCH,
    # on clean up branch, you have to explicitly define which env you want to clean up
    IS_CF_BRANCH,
    IS_LAYER_BRANCH,
    IS_LAMBDA_BRANCH,
    IS_PR_MERGE_EVENT,
    IS_PR_TARGET_MASTER_BRANCH,
)
from .runtime import IS_CI
from .paths import path_current_env_name_json
from .logger import logger


def _find_env() -> str:
    """
    Find which environment we should deploy to.
    """
    if IS_CI:
        # if it is in the delegated deployment repo,
        # then it is deploying to prod environment
        if os.environ["CODEBUILD_BUILD_ID"].startswith("{{ cookiecutter.package_name }}_admin-project"):
            return EnvEnum.prod.value

        # if it is a PR merge event and target is a master branch
        # then it is deploying to integration test environment
        if IS_PR_MERGE_EVENT and IS_PR_TARGET_MASTER_BRANCH:
            return EnvEnum.int.value
        # we don't do any deployment from PR merge event that
        # target is NOT a master branch
        elif IS_PR_MERGE_EVENT:
            raise NotImplementedError
        # if not a PR merge event
        else:
            # if it is a direct commit to master branch
            # then it is deploying to integration test environment
            if IS_MASTER_BRANCH:
                return EnvEnum.int.value
            # if it is a direct commit to application related branch
            # then it is deploying to dev environment
            elif (
                IS_FEATURE_BRANCH or IS_CF_BRANCH or IS_LAYER_BRANCH or IS_LAMBDA_BRANCH
            ):
                return EnvEnum.dev.value
            # if it is a direct commit to a release branch
            # then it is deploying to prod environment
            elif IS_RELEASE_BRANCH:
                return EnvEnum.prod.value
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
