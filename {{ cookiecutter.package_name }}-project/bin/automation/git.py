# -*- coding: utf-8 -*-

"""
This module implements the Git branch strategy related automation.

- main branch:
    - name pattern: exactly equal to ``main`` or ``master``
- feature branch:
    - name pattern: starts with ``feat`` or ``feature``
- release branch:
    - name pattern: starts with ``rls`` or ``release``
- cleanup branch:
    - usage: deploy AWS Lambda Function
    - name pattern: starts with ``clean`` or ``cleanup``
- cf branch:
    - usage: deploy AWS CloudFormation template
    - name pattern: starts with ``cf`` or ``cloudformation``
- layer branch:
    - usage: deploy AWS Lambda Layer
    - name pattern: starts with ``layer``
- lambda branch:
    - usage: deploy AWS Lambda Function
    - name pattern: starts with ``lbd`` or ``lambda``
- ecr branch:
    - usage: build ECR image
    - name pattern: starts with ``ecr``
"""

import os
import subprocess
from aws_codecommit import (
    ConventionalCommitParser,
    is_certain_semantic_commit,
)

from .paths import dir_project_root, temp_current_dir
from .runtime import IS_LOCAL, IS_CI
from .logger import logger


def get_git_branch_from_git_cli() -> str:
    """
    Use ``git`` CLI to get the current git branch.

    Run:

    .. code-block:: bash

        git branch --show-current
    """
    try:
        with temp_current_dir(dir_project_root):
            args = ["git", "branch", "--show-current"]
            res = subprocess.run(args, capture_output=True, check=True)
            branch = res.stdout.decode("utf-8").strip()
            return branch
    except Exception as e:
        logger.error(f"failed to get git branch from git CLI: {e}")
        return "unknown"


def get_git_commit_id_from_git_cli() -> str:
    """
    Use ``git`` CIL to get current git commit id.

    Run:

    .. code-block:: bash

        git rev-parse HEAD
    """
    try:
        with temp_current_dir(dir_project_root):
            args = ["git", "rev-parse", "HEAD"]
            res = subprocess.run(
                args,
                capture_output=True,
                check=True,
            )
            commit_id = res.stdout.decode("utf-8").strip()
            return commit_id
    except Exception as e:
        logger.error(f"failed to get git commit id from git CLI: {e}")
        return "unknown"


def get_commit_message_by_commit_id(commit_id: str) -> str:
    """
    Get the first line of commit message.

    Run:

    .. code-block:: bash

        git log --format=%B -n 1 ${commit_id}
    """
    args = ["git", "log", "--format=%B", "-n", "1", commit_id]
    response = subprocess.run(args, capture_output=True)
    message = response.stdout.decode("utf-8")
    message = message.strip().split("\n")[0].replace("'", "").replace('"', "").strip()
    return message


def is_master_branch(git_branch: str) -> bool:
    return git_branch.lower() in ["master", "main"]


def is_feature_branch(git_branch: str) -> bool:
    git_branch = git_branch.lower()
    return git_branch.startswith("feat") or git_branch.startswith("feature")


def is_int_branch(git_branch: str) -> bool:
    git_branch = git_branch.lower()
    return git_branch.startswith("int")


def is_release_branch(git_branch: str) -> bool:
    git_branch = git_branch.lower()
    return git_branch.startswith("rls") or git_branch.startswith("release")


def is_cleanup_branch(git_branch: str) -> bool:
    return git_branch.lower().startswith("cleanup")


def is_cf_branch(git_branch: str) -> bool:
    git_branch = git_branch.lower()
    return (
        git_branch.startswith("cf")
        or git_branch.startswith("cft")
        or git_branch.startswith("cloudformation")
    )


def is_layer_branch(git_branch: str) -> bool:
    return git_branch.lower().startswith("layer")


def is_lambda_branch(git_branch: str) -> bool:
    git_branch = git_branch.lower()
    return git_branch.startswith("lbd") or git_branch.startswith("lambda")


def is_ecr_branch(git_branch: str) -> bool:
    git_branch = git_branch.lower()
    return git_branch.startswith("ecr")


if IS_LOCAL:
    GIT_COMMIT_ID: str = get_git_commit_id_from_git_cli()
    GIT_COMMIT_MESSAGE: str = ""
    GIT_BRANCH_NAME: str = get_git_branch_from_git_cli()
    PR_FROM_BRANCH_NAME: str = ""
    PR_TO_BRANCH_NAME: str = ""
    GIT_EVENT: str = ""
elif IS_CI:
    GIT_COMMIT_ID: str = os.environ.get("CI_DATA_COMMIT_ID", "")
    GIT_COMMIT_MESSAGE: str = os.environ.get("CI_DATA_COMMIT_MESSAGE", "")
    GIT_BRANCH_NAME: str = os.environ.get("CI_DATA_BRANCH_NAME", "")
    PR_FROM_BRANCH_NAME: str = os.environ.get("CI_DATA_PR_FROM_BRANCH", "")
    PR_TO_BRANCH_NAME: str = os.environ.get("CI_DATA_PR_TO_BRANCH", "")
    GIT_EVENT: str = os.environ.get("CI_DATA_EVENT_TYPE", "")
else:
    raise NotImplementedError


def print_git_info():
    logger.info(f"Current git branch is ⤵️ {GIT_BRANCH_NAME!r}")
    logger.info(f"Current git commit is ✅ {GIT_COMMIT_ID!r}")


IS_MASTER_BRANCH: bool = is_master_branch(GIT_BRANCH_NAME)
IS_FEATURE_BRANCH: bool = is_feature_branch(GIT_BRANCH_NAME)
IS_INT_BRANCH: bool = is_int_branch(GIT_BRANCH_NAME)
IS_RELEASE_BRANCH: bool = is_release_branch(GIT_BRANCH_NAME)
IS_CLEAN_UP_BRANCH: bool = is_cleanup_branch(GIT_BRANCH_NAME)
IS_CF_BRANCH: bool = is_cf_branch(GIT_BRANCH_NAME)
IS_LAYER_BRANCH: bool = is_layer_branch(GIT_BRANCH_NAME)
IS_LAMBDA_BRANCH: bool = is_lambda_branch(GIT_BRANCH_NAME)
IS_ECR_BRANCH: bool = is_ecr_branch(GIT_BRANCH_NAME)

IS_PR_MERGE_EVENT: bool = GIT_EVENT == "pr_merged"
IS_PR_TARGET_MASTER_BRANCH: bool = is_master_branch(PR_TO_BRANCH_NAME)

IS_PR_SOURCE_CF_BRANCH: bool = is_cf_branch(PR_FROM_BRANCH_NAME)
IS_PR_SOURCE_LAYER_BRANCH: bool = is_layer_branch(PR_FROM_BRANCH_NAME)
IS_PR_SOURCE_LAMBDA_BRANCH: bool = is_lambda_branch(PR_FROM_BRANCH_NAME)


# ------------------------------------------------------------------------------
# use git commit message to identify what to clean up
# the commit message has to be ${stub}: ${description}
# ------------------------------------------------------------------------------
COMMIT_MESSAGE_HAS_CF: bool = False
COMMIT_MESSAGE_HAS_LBD: bool = False
if IS_CLEAN_UP_BRANCH:
    commit_parser = ConventionalCommitParser(types=["cf", "lbd"])
    has_cf_commit = is_certain_semantic_commit(
        GIT_COMMIT_MESSAGE, stub="cf", parser=commit_parser
    )
    has_lbd_commit = is_certain_semantic_commit(
        GIT_COMMIT_MESSAGE, stub="lbd", parser=commit_parser
    )
    if has_lbd_commit:
        COMMIT_MESSAGE_HAS_LBD = True
        if has_cf_commit:
            COMMIT_MESSAGE_HAS_CF = True

    if has_cf_commit is True and has_lbd_commit is False:
        raise ValueError(
            "You have to delete Lambda App first then you can delete CloudFormation Stack!"
        )
