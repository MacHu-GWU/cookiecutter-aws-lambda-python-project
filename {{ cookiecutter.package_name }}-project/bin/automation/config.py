# -*- coding: utf-8 -*-

"""
Config data related.
"""

import os
import pysecret

from aws_codecommit import better_boto

from {{ cookiecutter.package_name }}.config.init import config
from {{ cookiecutter.package_name }}.boto_ses import bsm

from .pyproject import pyproject
from .runtime import IS_CI
from .git import IS_RELEASE_BRANCH
from .logger import logger
from .emoji import Emoji
from .env import EnvEnum, CURRENT_ENV


def do_we_backup_prod_config(env_name: str) -> bool:
    # do it when it is working prod environment, and it is on release branch
    if (env_name == EnvEnum.prod) and IS_RELEASE_BRANCH:
        return True
    else:
        logger.info(
            f"{Emoji.red_circle} don't backup prod config, we only do it "
            f"on a PR from release branch to main branch in CI."
        )
        return False


@logger.block(
    msg="Backup prod Config",
    start_emoji=f"{Emoji.deploy} {Emoji.template}",
    end_emoji=f"{Emoji.deploy} {Emoji.template}",
    pipe=Emoji.template,
)
def backup_prod_config(
    env_name: str = CURRENT_ENV,
    check: bool = True,
):
    """
    Add label to parameter and backup the prod config data to S3
    after a release to production.

    Based on this AWS document `Working with parameter versions <https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-versions.html>`_,
    You can create and maintain up to 100 versions of a parameter. After you have
    created 100 versions of a parameter, each time you create a new version,
    the oldest version of the parameter is removed from history to make room
    for the new version. If your 100th old parameter has a critical production label,
    you cannot create new version anymore.

    In other word, parameter store is not a reliable storage for historical config
    backup. Everytime we release to production, we should create a backup for
    the prod config data on S3.
    """
    if check:
        if do_we_backup_prod_config(env_name) is False:
            return

    # read the parameter data that is used for this production deployment
    parameter = pysecret.Parameter.load(
        ssm_client=bsm.ssm_client,
        name=config.prod.parameter_name, # <- it is config.prod
        with_decryption=True,
    )

    # find the backup file s3 path
    basename = f"{EnvEnum.prod}-{pyproject.package_version}.json"
    s3path_prod_config = config.env.s3dir_config / basename
    logger.info(f"backup prod config data to {s3path_prod_config.basename}")
    logger.info(f"preview at: {s3path_prod_config.console_url}", indent=1)

    # create a backup of prod config data to s3
    # the config backup data should be immutable
    # it is possible that you want to deploy from older version (rollback)
    # in this situation, this function still runs, but it should not
    # overwrite the existing backup
    if s3path_prod_config.exists() is False:
        s3path_prod_config.write_text(
            parameter.Value,
            metadata=dict(
                release_version=pyproject.package_version,
            ),
            tags=dict(
                ProjectName=config.project_name,
                EnvName=env_name,
                PackageVersion=pyproject.package_version,
            ),
        )
        # in CI, post reply to the PR comment if possible
        if IS_CI:
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                content = "\n".join(
                    [
                        f"{Emoji.succeeded} {Emoji.template} **Backup prod config for version {pyproject.package_version!r}**",
                        f"",
                        f"- review [config file]({s3path_prod_config.console_url})",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
    else:
        logger.info(
            f"{Emoji.red_circle} config file already exists, "
            f"possibly it is not the first time releasing this version {pyproject.package_version!r}, "
            f"might be a rollback or a re-release, config file update won't happen",
            indent=1,
        )
        # in CI, post reply to the PR comment if possible
        if IS_CI:
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                content = "\n".join(
                    [
                        f"{Emoji.template} prod config for version {pyproject.package_version!r} "
                        "already exists, do nothing.",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
