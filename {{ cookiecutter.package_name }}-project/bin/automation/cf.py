# -*- coding: utf-8 -*-

"""
AWS CloudFormation related automation script.

.. note::

    All of the deployment automation function should have a required parameter
    ``env_name``. We need to ensure developer explicitly know what env they
    are dealing with
"""

import os

from aws_codecommit import better_boto
from aws_cloudformation import console

from {{ cookiecutter.package_name }}.iac.deploy import (
    deploy_cloudformation_stack as _deploy_cloudformation_stack,
    delete_cloudformation_stack as _delete_cloudformation_stack,
)
from {{ cookiecutter.package_name }}.boto_ses import bsm

from .git import (
    GIT_BRANCH_NAME,
    IS_CF_BRANCH,
    IS_INT_BRANCH,
    IS_RELEASE_BRANCH,
    IS_CLEAN_UP_BRANCH,
    COMMIT_MESSAGE_HAS_CF,
)
from .runtime import IS_CI
from .logger import logger
from .emoji import Emoji
from .env import CURRENT_ENV
from .cf_rule import (
    do_we_deploy_cf,
    do_we_delete_cf,
)


@logger.block(
    msg="Deploy CloudFormation Stack",
    start_emoji=f"{Emoji.deploy} {Emoji.cloudformation}",
    end_emoji=f"{Emoji.deploy} {Emoji.cloudformation}",
    pipe=Emoji.cloudformation,
)
def deploy_cloudformation_stack(
    env_name: str = CURRENT_ENV,
    check: bool = True,
):
    try:
        if check:
            if (
                do_we_deploy_cf(
                    env_name=env_name,
                    is_ci_runtime=IS_CI,
                    branch_name=GIT_BRANCH_NAME,
                    is_cf_branch=IS_CF_BRANCH,
                    is_int_branch=IS_INT_BRANCH,
                    is_release_branch=IS_RELEASE_BRANCH,
                )
                is False
            ):
                return
        stack_name = _deploy_cloudformation_stack(env_name, dry_run=False)
        logger.info(f"{Emoji.succeeded} Deploy CloudFormation stack succeeded!")
        # in CI, post the cloudformation stack url to the PR comment if possible
        if IS_CI:
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                stacks_view_console_url = console.get_stacks_view_console_url(
                    stack_name=stack_name,
                    aws_region=bsm.aws_region,
                )
                content = "\n".join(
                    [
                        f"{Emoji.succeeded} {Emoji.cloudformation}️ **Deploy CloudFormation stack succeeded**",
                        f"",
                        f"- review [CloudFormation stack]({stacks_view_console_url})",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
    except Exception as e:
        logger.error(f"{Emoji.failed} Deploy CloudFormation stack failed!")
        # in CI, post the error message to the PR comment if possible
        if IS_CI:
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                content = "\n".join(
                    [
                        f"{Emoji.failed} Deploy CloudFormation stack failed!",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
        raise e


@logger.block(
    msg="Delete CloudFormation Stack",
    start_emoji=f"{Emoji.delete} {Emoji.cloudformation}",
    end_emoji=f"{Emoji.delete} {Emoji.cloudformation}",
    pipe=Emoji.cloudformation,
)
def delete_cloudformation_stack(
    env_name: str = CURRENT_ENV,
    check: bool = True,
):
    try:
        if check:
            if (
                do_we_delete_cf(
                    env_name=env_name,
                    is_ci_runtime=IS_CI,
                    is_clean_up_branch=IS_CLEAN_UP_BRANCH,
                    commit_message_has_cf=COMMIT_MESSAGE_HAS_CF,
                )
                is False
            ):
                return
        stack_name = _delete_cloudformation_stack(env_name)
        logger.info(f"{Emoji.succeeded} Delete CloudFormation stack succeeded!")
        if IS_CI:
            # post reply to codecommit PR thread, if possible
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                stacks_view_console_url = console.get_stacks_view_console_url(
                    stack_name=stack_name,
                    aws_region=bsm.aws_region,
                )
                content = "\n".join(
                    [
                        f"{Emoji.succeeded} {Emoji.cloudformation}️ **Delete CloudFormation stack succeeded**",
                        f"",
                        f"- review [CloudFormation stack]({stacks_view_console_url})",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
    except Exception as e:
        logger.error(f"{Emoji.failed} Delete CloudFormation stack failed!")
        if IS_CI:
            # post reply to codecommit PR thread, if possible
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                content = "\n".join(
                    [
                        f"{Emoji.failed} Delete CloudFormation stack failed!",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
        raise e
