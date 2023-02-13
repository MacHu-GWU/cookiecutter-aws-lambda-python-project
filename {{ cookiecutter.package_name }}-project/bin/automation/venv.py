# -*- coding: utf-8 -*-

"""
Virtualenv management.
"""

import subprocess

from .paths import dir_venv
from .pyproject import pyproject
from .logger import logger
from .emoji import Emoji


@logger.block(
    msg="Create Virtual Environment",
    start_emoji=Emoji.python,
    end_emoji=Emoji.python,
    pipe=Emoji.python,
)
def poetry_venv_create():
    """
    .. code-block:: bash

        $ poetry config virtualenvs.in-project true --local
        $ poetry env use python${X}.${Y}
    """
    if not dir_venv.exists():
        subprocess.run(
            ["poetry", "config", "virtualenvs.in-project", "true", "--local"],
            check=True,
        )
        subprocess.run(
            ["poetry", "env", "use", f"python{pyproject.python_version}"],
            check=True,
        )
        logger.info("done")
    else:
        logger.info(f"{dir_venv} already exists, do nothing.")


@logger.block(
    msg="Create Virtual Environment",
    start_emoji=Emoji.python,
    end_emoji=Emoji.python,
    pipe=Emoji.python,
)
def virtualenv_venv_create():
    """
    .. code-block:: bash

        $ virtualenv -p python${X}.${Y} ./.venv
    """
    if not dir_venv.exists():
        subprocess.run(
            ["virtualenv", "-p", f"python{pyproject.python_version}", f"{dir_venv}"],
            check=True,
        )
        logger.info("done")
    else:
        logger.info(f"{dir_venv} already exists, do nothing.")


@logger.block(
    msg="Remove Virtual Environment",
    start_emoji=Emoji.python,
    end_emoji=Emoji.python,
    pipe=Emoji.python,
)
def venv_remove():
    """
    .. code-block:: bash

        $ rm -r ./.venv
    """
    if dir_venv.exists():
        subprocess.run(["rm", "-r", f"{dir_venv}"])
        logger.info(f"done! {dir_venv} is removed.")
    else:
        logger.info(f"{dir_venv} doesn't exists, do nothing.")
