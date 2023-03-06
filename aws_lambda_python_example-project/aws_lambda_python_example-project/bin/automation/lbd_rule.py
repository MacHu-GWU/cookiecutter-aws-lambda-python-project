# -*- coding: utf-8 -*-

from .env import EnvEnum
from .logger import logger
from .emoji import Emoji
from .cleanup_rule import do_we_delete_this_resource_in_local


def do_we_build_lambda_layer(
    is_ci_runtime: bool,
    branch_name: str,
    is_layer_branch: bool,
) -> bool:
    if is_ci_runtime:  # in CI, we only build layer from layer branch
        if is_layer_branch:
            pass
        else:
            logger.info(
                f"{Emoji.red_circle} don't build Lambda layer, "
                f"we only build layer from CI environment on a 'layer' branch, "
                f"now we are on {branch_name!r} branch."
            )
            return False
    else:  # always allow build layer on local
        return True


def do_we_publish_lambda_layer(
    is_ci_runtime: bool,
    branch_name: str,
    is_layer_branch: bool,
) -> bool:
    if is_ci_runtime:
        if is_layer_branch:
            return True
        else:
            logger.info(
                f"{Emoji.red_circle} don't publish layer, "
                f"we only publish layer from CI environment on a 'layer' branch, "
                f"now we are on {branch_name!r} branch."
            )
            return False
    else:
        logger.info(
            f"{Emoji.red_circle} don't publish layer, "
            f"we only publish layer from CI environment, "
            f"now we are on local development environment."
        )
        return False


def do_we_deploy_lambda(
    env_name: str,
    is_ci_runtime: bool,
    branch_name: str,
    is_lambda_branch: bool,
    is_int_branch: bool,
    is_release_branch: bool,
) -> bool:
    if is_ci_runtime:
        if is_lambda_branch or is_int_branch or is_release_branch:  # dev  # int  # prod
            return True
        else:
            logger.info(
                f"{Emoji.red_circle} don't deploy lambda app, "
                f"we only deploy lambda app from CI environment on "
                f"'lambda', 'int' or 'release' branch, "
                f"now we are on {branch_name!r} branch.",
            )
            return False
    else:  # always allow that deploy lambda from local
        if env_name == EnvEnum.prod.value:
            user_input = input(
                f"you are trying to deploy Lambda to {EnvEnum.prod.value!r} locally, "
                f"enter 'YES' to confirm: "
            )
            if user_input.strip() == "YES":
                return True
            else:
                logger.info(
                    f"{Emoji.red_circle} don't deploy Lambda. "
                    f"because user input {user_input!r} is not 'YES'."
                )
                return False
        else:
            return True


def _do_we_delete_lambda_in_ci(
    is_clean_up_branch: bool,
    commit_message_has_lbd: bool,
) -> bool:
    if is_clean_up_branch is False:
        logger.info(
            f"{Emoji.red_circle} don't delete Lambda App, "
            f"we only delete Lambda App from a 'cleanup' branch."
        )
        return False

    if commit_message_has_lbd is False:
        logger.info(
            f"{Emoji.red_circle} don't delete Lambda App, "
            "we only delete Lambda App from a 'cleanup' branch "
            "when the commit message include 'lbd'"
        )
        return False

    return True


def do_we_delete_lambda(
    env_name: str,
    is_ci_runtime: bool,
    is_clean_up_branch: bool,
    commit_message_has_lbd: bool,
) -> bool:
    """
    Check if we should delete Lambda App.
    """
    if is_ci_runtime:
        return _do_we_delete_lambda_in_ci(
            is_clean_up_branch=is_clean_up_branch,
            commit_message_has_lbd=commit_message_has_lbd,
        )
    else:
        return do_we_delete_this_resource_in_local(
            resource_name="Lambda App",
            env_name=env_name,
            is_clean_up_branch=is_clean_up_branch,
        )
