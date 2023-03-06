# -*- coding: utf-8 -*-

from .logger import logger
from .emoji import Emoji


def _do_we_run_unit_test_in_ci(
    branch_name: str,
    is_master_branch: bool,
    is_feature_branch: bool,
    is_lambda_branch: bool,
    is_ecr_branch: bool,
    is_int_branch: bool,
) -> bool:
    """
    In CI, we only run unit test when it is a branch that may cause
    application code change.

    we don't run unit test in prod environment because unit test may
    change the state of the cloud resources, and it should be already
    thoroughly tested in int environment.
    """
    if (
        is_master_branch
        or is_feature_branch
        or is_lambda_branch
        or is_ecr_branch
        or is_int_branch
    ):
        return True
    else:
        logger.info(
            f"{Emoji.red_circle} don't run unit test, we only run unit test on a "
            f"'master', 'feature', 'lambda', 'ecr', 'int' branch in CI, "
            f"we are now on {branch_name!r} branch"
        )
        return False


def do_we_run_unit_test(
    is_ci_runtime: bool,
    branch_name: str,
    is_master_branch: bool,
    is_feature_branch: bool,
    is_lambda_branch: bool,
    is_ecr_branch: bool,
    is_int_branch: bool,
) -> bool:
    """
    Check if we should run unit test or coverage test.
    """
    if is_ci_runtime:
        return _do_we_run_unit_test_in_ci(
            branch_name=branch_name,
            is_master_branch=is_master_branch,
            is_feature_branch=is_feature_branch,
            is_lambda_branch=is_lambda_branch,
            is_ecr_branch=is_ecr_branch,
            is_int_branch=is_int_branch,
        )
    else:  # always run unit test on Local
        return True


def _do_we_run_int_test_in_ci(
    branch_name: str,
    is_int_branch: bool,
) -> bool:
    """
    In CI, we only run integration test on 'int' branch (also 'int' environment).
    """
    if is_int_branch:
        return True
    else:
        logger.info(
            f"{Emoji.red_circle} don't run integration test, "
            f"we only run integration test on a 'int' branch in CI, "
            f"we are now on {branch_name!r} branch."
        )
        return False


def do_we_run_int_test(
    is_ci_runtime: bool,
    branch_name: str,
    is_int_branch: bool,
) -> bool:
    """
    Check if we should run integration test.
    """
    if is_ci_runtime:
        return _do_we_run_int_test_in_ci(
            branch_name=branch_name,
            is_int_branch=is_int_branch,
        )
    else:  # always run test on Local
        return True
