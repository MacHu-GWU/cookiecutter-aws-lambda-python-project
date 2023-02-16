# -*- coding: utf-8 -*-

"""
This module automates dependencies management.

We use `Python poetry <https://python-poetry.org/>`_ to ensure determinative dependencies.

"""

import typing as T
import json
import subprocess
from pathlib import Path

from .paths import (
    dir_project_root,
    bin_pip,
    path_requirements_main,
    path_requirements_dev,
    path_requirements_test,
    path_requirements_doc,
    path_requirements_automation,
    path_poetry_lock,
    path_poetry_lock_hash_json,
    temp_current_dir,
)
from .logger import logger
from .emoji import Emoji
from .helpers import sha256_of_bytes
from .runtime import IS_CI


@logger.block(
    msg="Resolve Dependencies Tree",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def poetry_lock():
    """
    Run:

    .. code-block:: bash

        poetry lock

    This command will resolve the dependencies defined in the ``pyproject.toml``
    file, and write the resolved versions to the ``poetry.lock`` file.
    You have to run this everytime you changed the ``pyproject.toml`` file.
    And you should commit the latest ``poetry.lock`` file to git.

    Ref:

    - poetry lock: https://python-poetry.org/docs/cli/#lock
    """
    with temp_current_dir(dir_project_root):
        subprocess.run(["poetry", "lock"])


@logger.block(
    msg="Install main dependencies and Package itself",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def poetry_install():
    """
    Run:

    .. code-block:: bash

        poetry install

    Ref:

    - poetry install: https://python-poetry.org/docs/cli/#install
    """
    subprocess.run(["poetry", "install"], check=True)


@logger.block(
    msg="Install dev dependencies",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def poetry_install_dev():
    """
    Run:

    .. code-block:: bash

        poetry install --with dev

    Ref:

    - poetry install: https://python-poetry.org/docs/cli/#install
    """
    subprocess.run(["poetry", "install", "--with", "dev"], check=True)


@logger.block(
    msg="Install test dependencies",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def poetry_install_test():
    """
    Run:

    .. code-block:: bash

        poetry install --with test

    Ref:

    - poetry install: https://python-poetry.org/docs/cli/#install
    """
    subprocess.run(["poetry", "install", "--with", "test"], check=True)


@logger.block(
    msg="Install doc dependencies",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def poetry_install_doc():
    """
    Run:

    .. code-block:: bash

        poetry install --with doc

    Ref:

    - poetry install: https://python-poetry.org/docs/cli/#install
    """
    subprocess.run(["poetry", "install", "--with", "doc"], check=True)


@logger.block(
    msg="Install all dependencies for dev, test, doc",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def poetry_install_all():
    """
    Run:

    .. code-block:: bash

        poetry install --with dev,test,doc

    Ref:

    - poetry install: https://python-poetry.org/docs/cli/#install
    """
    subprocess.run(["poetry", "install", "--with", "dev,test,doc"], check=True)


def _do_we_need_poetry_export(current_poetry_lock_hash: str) -> bool:
    """
    ``poetry export`` is an expensive command. We would like to use cache
    mechanism to avoid unnecessary export.

    Everytime we run :func:`_poetry_export`, at the end, it will write the
    sha256 hash of the ``poetry.lock`` to the ``.poetry-lock-hash.json`` cache file.
    It locates at the repo root directory. This function will compare the
    sha256 hash of the current ``poetry.lock`` to the value stored in the cache file.
    If they don't match, it means that the ``poetry.lock`` has been changed,
    so we should run :func:`_poetry_export` again.

    The content of ``.poetry-lock-hash.json`` looks like::

        {
            "hash": "sha256-hash-of-the-poetry.lock-file",
            "description": "DON'T edit this file manually!"
        }

    Ref:

    - poetry export: https://python-poetry.org/docs/cli/#export

    :param current_poetry_lock_hash: the sha256 hash of the current ``poetry.lock`` file
    """
    if path_poetry_lock_hash_json.exists():
        # read the previous poetry lock hash from cache file
        cached_poetry_lock_hash = json.loads(path_poetry_lock_hash_json.read_text())[
            "hash"
        ]
        return current_poetry_lock_hash != cached_poetry_lock_hash
    else:
        # do poetry export if the cache file not found
        return True


def _poetry_export_group(group: str, path: Path):
    """
    Export dependency group to given file.

    :param group: dependency group name, for example dev dependencies are defined
        in the ``[tool.poetry.group.dev]`` and ``[tool.poetry.group.dev.dependencies]``
        sections of he ``pyproject.toml`` file.
    :param path: the path to the exported ``requirements.txt`` file.
    """
    subprocess.run(
        [
            "poetry",
            "export",
            "--format",
            "requirements.txt",
            "--output",
            f"{path}",
            "--only",
            group,
        ],
        check=True,
    )


def _poetry_export(current_poetry_lock_hash: str):
    """
    Run ``poetry export --format requirements.txt ...`` command and write
    the sha256 hash of the current ``poetry.lock`` file to the cache file.

    :param current_poetry_lock_hash: the sha256 hash of the current ``poetry.lock`` file
    """
    # export the main dependencies
    logger.info(f"export to {path_requirements_main.name}")
    path_requirements_main.unlink(missing_ok=True)
    subprocess.run(
        [
            "poetry",
            "export",
            "--format",
            "requirements.txt",
            "--output",
            f"{path_requirements_main}",
        ],
        check=True,
    )

    # export dev, test, doc dependencies
    for group, path in [
        ("dev", path_requirements_dev),
        ("test", path_requirements_test),
        ("doc", path_requirements_doc),
    ]:
        logger.info(f"export to {path.name}")
        path.unlink(missing_ok=True)
        _poetry_export_group(group, path)

    # write the ``poetry.lock`` hash to the cache file
    path_poetry_lock_hash_json.write_text(
        json.dumps(
            {
                "hash": current_poetry_lock_hash,
                "description": "DON'T edit this file manually!",
            },
            indent=4,
        )
    )


@logger.block(
    msg="Export resolved dependencies to req-***.txt file",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def poetry_export():
    poetry_lock_hash = sha256_of_bytes(path_poetry_lock.read_bytes())
    if _do_we_need_poetry_export(poetry_lock_hash):
        _poetry_export(poetry_lock_hash)
    else:
        logger.info("already did, do nothing")


def _try_poetry_export():
    """
    This is a silent version of :func:`poetry_export`. It is called before
    running ``pip install -r requirements-***.txt`` command. It ensures that
    those exported ``requirements-***.txt`` file exists.
    """
    poetry_lock_hash = sha256_of_bytes(path_poetry_lock.read_bytes())
    if _do_we_need_poetry_export(poetry_lock_hash):
        _poetry_export(poetry_lock_hash)


def _quite_pip_install_in_ci(args: T.List[str]):
    """
    Add a cli argument to disable output for ``pip install`` command.

    We only need to disable ``pip install`` output in CI, because we don't
    want to see long list of installation messages in CI.
    """
    args.append("--disable-pip-version-check")
    if IS_CI:
        args.append("--quiet")


@logger.block(
    msg="Install main dependencies and Package itself",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def pip_install():
    """
    Run:

    .. code-block:: bash

        pip install -e . --no-deps

    Ref:

    - pip install: https://pip.pypa.io/en/stable/cli/pip_install/#options
    """
    _try_poetry_export()

    args = [f"{bin_pip}", "install", "-e", f"{dir_project_root}", "--no-deps"]
    _quite_pip_install_in_ci(args)
    subprocess.run(args, check=True)

    args = [f"{bin_pip}", "install", "-r", f"{path_requirements_main}"]
    _quite_pip_install_in_ci(args)
    subprocess.run(args, check=True)


@logger.block(
    msg="Install dev dependencies",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def pip_install_dev():
    """
    Run:

    .. code-block:: bash

        pip install -r requirements-dev.txt
    """
    _try_poetry_export()

    args = [f"{bin_pip}", "install", "-r", f"{path_requirements_dev}"]
    _quite_pip_install_in_ci(args)
    subprocess.run(
        args,
        check=True,
    )


@logger.block(
    msg="Install test dependencies",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def pip_install_test():
    """
    Run:

    .. code-block:: bash

        pip install -r requirements-test.txt
    """
    _try_poetry_export()

    args = [f"{bin_pip}", "install", "-r", f"{path_requirements_test}"]
    _quite_pip_install_in_ci(args)
    subprocess.run(
        args,
        check=True,
    )


@logger.block(
    msg="Install doc dependencies",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def pip_install_doc():
    """
    Run:

    .. code-block:: bash

        pip install -r requirements-doc.txt
    """
    _try_poetry_export()

    args = [f"{bin_pip}", "install", "-r", f"{path_requirements_doc}"]
    _quite_pip_install_in_ci(args)
    subprocess.run(
        args,
        check=True,
    )


@logger.block(
    msg="Install automation dependencies",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def pip_install_automation():
    """
    Run:

    .. code-block:: bash

        pip install -r requirements-automation.txt
    """
    args = [f"{bin_pip}", "install", "-r", f"{path_requirements_automation}"]
    _quite_pip_install_in_ci(args)
    subprocess.run(
        args,
        check=True,
    )


@logger.block(
    msg="Install all dependencies",
    start_emoji=Emoji.install,
    end_emoji=Emoji.install,
    pipe=Emoji.install,
)
def pip_install_all():
    """
    Run:

    .. code-block:: bash

        pip install -r requirements-main.txt
        pip install -r requirements-dev.txt
        pip install -r requirements-test.txt
        pip install -r requirements-doc.txt
        pip install -r requirements-automation.txt
    """
    _try_poetry_export()

    subprocess.run(
        [f"{bin_pip}", "install", "-e", f"{dir_project_root}", "--no-deps"],
        check=True,
    )

    for path in [
        path_requirements_main,
        path_requirements_dev,
        path_requirements_test,
        path_requirements_doc,
        path_requirements_automation,
    ]:
        args = [f"{bin_pip}", "install", "-r", f"{path}"]
        _quite_pip_install_in_ci(args)
        subprocess.run(
            args,
            check=True,
        )
