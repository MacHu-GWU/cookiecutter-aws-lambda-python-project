# -*- coding: utf-8 -*-

import subprocess

from .paths import (
    bin_pytest,
    dir_tests,
    dir_tests_int,
    dir_htmlcov,
)
from .pyproject import pyproject
from .runtime import IS_CI
from .git import (
    GIT_BRANCH_NAME,
    IS_MASTER_BRANCH,
    IS_FEATURE_BRANCH,
    IS_LAMBDA_BRANCH,
    IS_ECR_BRANCH,
    IS_PR_MERGE_EVENT,
    IS_PR_SOURCE_LAMBDA_BRANCH,
    IS_PR_TARGET_MASTER_BRANCH,
)
from .logger import logger
from .emoji import Emoji


def do_we_run_unit_test() -> bool:
    """
    Check if we should run unit test or coverage test.
    """
    if IS_CI:
        # in CI, we only run unit test when it is a feature branch, or lambda branch
        # which implies application code change.
        # we don't run unit test in prod environment because unit test may
        # change the state of the cloud resources, and it should be already
        # thoroughly tested in int environment
        if (
            IS_MASTER_BRANCH
            or IS_FEATURE_BRANCH
            or IS_LAMBDA_BRANCH
            or IS_ECR_BRANCH
        ):
            return True
        else:
            logger.info(
                f"{Emoji.red_circle} don't run test, "
                f"we only run test on master, feature, layer, release branch in CI, "
                f"we are now on {GIT_BRANCH_NAME!r} branch"
            )
            return False
    else:  # always run test on Local
        return True


@logger.block(
    msg="Run Unit Test",
    start_emoji=Emoji.test,
    end_emoji=Emoji.test,
    pipe=Emoji.test,
)
def run_unit_test():
    if do_we_run_unit_test():
        try:
            args = [
                f"{bin_pytest}",
                f"{dir_tests}",
                "-s",
            ]
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
def run_cov_test():
    if do_we_run_unit_test():
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
            subprocess.run(args, check=True)
            logger.info(f"{Emoji.succeeded} Code Coverage Test Succeeded!")
        except Exception as e:
            logger.error(f"{Emoji.error} Code Coverage Test Failed!")
            raise e


def do_we_run_int_test() -> bool:
    """
    Check if we should run integration test.
    """
    if IS_CI:
        if IS_PR_MERGE_EVENT:
            # only run integration test when merging from lambda branch
            # to master branch.
            # because after it merge to master branch, it is supposed to
            # deploy to int environment.
            if IS_PR_TARGET_MASTER_BRANCH:
                if IS_PR_SOURCE_LAMBDA_BRANCH:
                    return True
                else:
                    logger.info(
                        f"{Emoji.red_circle} don't run integration test, "
                        f"it is a PR merge event, and target is master branch, "
                        f"but it is not from lambda branch.",
                    )
            else:
                logger.info(
                    f"{Emoji.red_circle} don't run integration test, "
                    f"it is a PR merge event, but it is not merge to master branch."
                )
                return False
        else: # not a PR merge event
            if IS_MASTER_BRANCH:
                # only run integration test on master branch
                # we don't run integration test in prod environment
                # it should be already thoroughly tested in int environment
                return True
            else:
                logger.info(
                    f"{Emoji.red_circle} don't run integration test, "
                    f"we only run integration test on master branch in CI, "
                    f"we are now on {GIT_BRANCH_NAME!r} branch"
                )
                return False
    else:  # always run test on Local
        return True


@logger.block(
    msg="Run Integration Test",
    start_emoji=Emoji.test,
    end_emoji=Emoji.test,
    pipe=Emoji.test,
)
def run_int_test():
    if do_we_run_int_test():
        args = [
            f"{bin_pytest}",
            f"{dir_tests_int}",
            "-s",
        ]
        try:
            subprocess.run(args, check=True)
            logger.info(f"{Emoji.succeeded} Integration Test Succeeded!")
        except Exception as e:
            logger.error(f"{Emoji.error} Integration Test Failed!")
            raise e
