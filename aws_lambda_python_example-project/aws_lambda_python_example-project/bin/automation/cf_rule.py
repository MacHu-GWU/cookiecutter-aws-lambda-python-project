# -*- coding: utf-8 -*-

from .env import EnvEnum
from .logger import logger
from .emoji import Emoji
from .cleanup_rule import do_we_delete_this_resource_in_local


def _do_we_deploy_cf_in_ci(
    env_name: str,
    branch_name: str,
    is_cf_branch: bool,
    is_int_branch: bool,
    is_release_branch: bool,
) -> bool:
    if is_cf_branch or is_int_branch or is_release_branch:
        return True
    else:
        logger.info(
            f"{Emoji.red_circle} don't deploy CloudFormation. "
            f"in CI runtime, we only deploy CloudFormation from a "
            f"'cf' or 'int' or 'release' branch. "
            f"now it is {env_name!r} env and {branch_name!r} branch."
        )
        return False


def _do_we_deploy_cf_in_local(
    env_name: str,
    branch_name: str,
    is_cf_branch: bool,
    is_int_branch: bool,
    is_release_branch: bool,
) -> bool:
    if env_name in [EnvEnum.dev.value, EnvEnum.int.value]:
        if is_cf_branch or is_int_branch or is_release_branch:
            return True
        else:
            logger.info(
                f"{Emoji.red_circle} don't deploy CloudFormation. "
                f"on {EnvEnum.dev.value!r} and {EnvEnum.int.value!r} env, "
                "we only deploy CloudFormation from a 'cf' or 'int' or 'release' branch, "
                f"now it is {env_name!r} env and {branch_name!r} branch."
            )
            return False
    elif env_name == EnvEnum.prod.value:
        if is_release_branch:
            user_input = input(
                f"you are trying to deploy CloudFormation to {EnvEnum.prod.value!r} locally, "
                f"enter 'YES' to confirm: "
            )
            if user_input.strip() == "YES":
                return True
            else:
                logger.info(
                    f"{Emoji.red_circle} don't deploy CloudFormation. "
                    f"because user input {user_input!r} is not 'YES'."
                )
                return False
    else:
        raise NotImplementedError


def do_we_deploy_cf(
    env_name: str,
    is_ci_runtime: bool,
    branch_name: str,
    is_cf_branch: bool,
    is_int_branch: bool,
    is_release_branch: bool,
) -> bool:
    # CI runtime
    if is_ci_runtime:
        return _do_we_deploy_cf_in_ci(
            env_name=env_name,
            branch_name=branch_name,
            is_cf_branch=is_cf_branch,
            is_int_branch=is_int_branch,
            is_release_branch=is_release_branch,
        )
    else:
        return _do_we_deploy_cf_in_local(
            env_name=env_name,
            branch_name=branch_name,
            is_cf_branch=is_cf_branch,
            is_int_branch=is_int_branch,
            is_release_branch=is_release_branch,
        )


def _do_we_delete_cf_in_ci(
    is_clean_up_branch: bool,
    commit_message_has_cf: bool,
) -> bool:
    if is_clean_up_branch is False:
        logger.info(
            f"{Emoji.red_circle} don't delete CloudFormation, "
            f"we only delete CloudFormation from a 'cleanup' branch"
        )
        return False

    if commit_message_has_cf is False:
        logger.info(
            f"{Emoji.red_circle} don't delete CloudFormation, "
            f"we only delete CloudFormation from a 'cleanup' branch"
            "when the commit message include 'cf'."
        )
        return False

    return True


def do_we_delete_cf(
    env_name: str,
    is_ci_runtime: bool,
    is_clean_up_branch: bool,
    commit_message_has_cf: bool,
) -> bool:
    """
    Check if we should delete AWS Cloudformation template.
    """
    if is_ci_runtime:
        return _do_we_delete_cf_in_ci(
            is_clean_up_branch=is_clean_up_branch,
            commit_message_has_cf=commit_message_has_cf,
        )
    else:
        return do_we_delete_this_resource_in_local(
            resource_name="CloudFormation",
            env_name=env_name,
            is_clean_up_branch=is_clean_up_branch,
        )
