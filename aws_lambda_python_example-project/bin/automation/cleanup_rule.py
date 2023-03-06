# -*- coding: utf-8 -*-

from .env import EnvEnum
from .logger import logger
from .emoji import Emoji


def do_we_delete_this_resource_in_local(
    resource_name: str,
    env_name: str,
    is_clean_up_branch: bool,
) -> bool:
    """
    We only delete resources from a cleanup branch, and the branch name has to
    explicitly define which environment to delete from. A valid ``cleanup``
    branch name should be ``cleanup/${env_name}`` or ``cleanup/${env_name}/${description}``.
    """
    if is_clean_up_branch:
        user_input = input(
            f"trying to delete {resource_name} from {env_name!r} environment locally, "
            f"enter 'YES' to confirm: "
        )
        if user_input.strip() == "YES":
            if env_name == EnvEnum.prod.value:
                user_input = input(
                    f"it is {env_name!r} are you really sure? "
                    f"enter 'I CONFIRM' to confirm: "
                )
                if user_input.strip() == "I CONFIRM":
                    return True
                else:
                    logger.info(
                        f"{Emoji.red_circle} don't delete {resource_name}. "
                        f"because user input {user_input!r} is not 'I CONFIRM'."
                    )
                    return False
            else:
                return True
        else:
            logger.info(
                f"{Emoji.red_circle} don't delete {resource_name}. "
                f"because user input {user_input!r} is not 'YES'."
            )
            return False
    else:
        logger.info(
            f"{Emoji.red_circle} don't delete {resource_name}, "
            f"we only delete {resource_name} from a 'cleanup' branch"
        )
        return False
