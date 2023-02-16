# -*- coding: utf-8 -*-

import subprocess

from .paths import (
    bin_pytest,
    dir_tests,
    dir_tests_int,
    dir_htmlcov,
    dir_project_root,
    temp_current_dir,
)
from .pyproject import pyproject
from .runtime import IS_CI
from .git import (
    GIT_BRANCH_NAME,
    IS_MASTER_BRANCH,
    IS_FEATURE_BRANCH,
    IS_INT_BRANCH,
    IS_LAMBDA_BRANCH,
    IS_ECR_BRANCH,
)
from .logger import logger
from .emoji import Emoji
from .tests_rule import (
    do_we_run_unit_test,
    do_we_run_int_test,
)


@logger.block(
    msg="Run Unit Test",
    start_emoji=Emoji.test,
    end_emoji=Emoji.test,
    pipe=Emoji.test,
)
def run_unit_test(
    check: bool = True,
):
    if check:
        if (
            do_we_run_unit_test(
                branch_name=GIT_BRANCH_NAME,
                is_master_branch=IS_MASTER_BRANCH,
                is_feature_branch=IS_FEATURE_BRANCH,
                is_lambda_branch=IS_LAMBDA_BRANCH,
                is_ecr_branch=IS_ECR_BRANCH,
                is_int_branch=IS_INT_BRANCH,
            )
            is False
        ):
            return

    try:
        args = [
            f"{bin_pytest}",
            f"{dir_tests}",
            "-s",
        ]
        with temp_current_dir(
            dir_project_root
        ):  # ensure current dir is the project root
            subprocess.run(args, check=True)
        logger.info(f"{Emoji.start_timer} Unit Test Succeeded!")
    except Exception as e:
        logger.error(f"{Emoji.error} Unit Test Failed!")
        raise e


@logger.block(
    msg="Run Code Coverage Test",
    start_emoji=Emoji.test,
    end_emoji=Emoji.test,
    pipe=Emoji.test,
)
def run_cov_test(
    check: bool = True,
):
    if check:
        if (
            do_we_run_unit_test(
                is_ci_runtime=IS_CI,
                branch_name=GIT_BRANCH_NAME,
                is_master_branch=IS_MASTER_BRANCH,
                is_feature_branch=IS_FEATURE_BRANCH,
                is_lambda_branch=IS_LAMBDA_BRANCH,
                is_ecr_branch=IS_ECR_BRANCH,
                is_int_branch=IS_INT_BRANCH,
            )
            is False
        ):
            return

    args = [
        f"{bin_pytest}",
        f"{dir_tests}",
        "-s",
        f"--cov={pyproject.package_name}",
        "--cov-report",
        "term-missing",
        "--cov-report",
        f"html:{dir_htmlcov}",
    ]
    try:
        with temp_current_dir(
            dir_project_root
        ):  # ensure current dir is the project root
            subprocess.run(args, check=True)
        logger.info(f"{Emoji.succeeded} Code Coverage Test Succeeded!")
    except Exception as e:
        logger.error(f"{Emoji.error} Code Coverage Test Failed!")
        raise e


@logger.block(
    msg="Run Integration Test",
    start_emoji=Emoji.test,
    end_emoji=Emoji.test,
    pipe=Emoji.test,
)
def run_int_test(
    check: bool = True,
):
    if check:
        if (
            do_we_run_int_test(
                is_ci_runtime=IS_CI,
                branch_name=GIT_BRANCH_NAME,
                is_int_branch=IS_INT_BRANCH,
            )
            is False
        ):
            return

    args = [
        f"{bin_pytest}",
        f"{dir_tests_int}",
        "-s",
    ]
    try:
        with temp_current_dir(
            dir_project_root
        ):  # ensure current dir is the project root
            subprocess.run(args, check=True)
        logger.info(f"{Emoji.succeeded} Integration Test Succeeded!")
    except Exception as e:
        logger.error(f"{Emoji.error} Integration Test Failed!")
        raise e
