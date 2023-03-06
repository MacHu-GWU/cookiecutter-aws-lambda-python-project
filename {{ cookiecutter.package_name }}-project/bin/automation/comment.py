# -*- coding: utf-8 -*-

"""
This module implements the comment bot logics.

Comment bot is a program that runs in CI build job and automatically post comments
to Pull Request and Code Review thread, provides rich information about the build.
"""

import os
from aws_codecommit import better_boto


def post_comment_reply(
    message: str,
    is_ci: bool,
):
    """
    Post a reply to the CodeCommit PR thread.

    It gets the CodeCommit comment id from environment variable ``CI_DATA_COMMENT_ID``,
    this environment variable is set by the ``codebuild.start_build_job()`` API,

    https://github.com/MacHu-GWU/aws_ci_bot-project

    :param message: the body of comment in Markdown format.
    :param is_ci: we only post reply from CI build job
    """
    if is_ci is False:
        return

    from {{ cookiecutter.package_name }}.boto_ses import bsm

    if is_ci:
        comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
        if comment_id:
            better_boto.post_comment_reply(
                bsm=bsm,
                in_reply_to=comment_id,
                content=message,
            )
