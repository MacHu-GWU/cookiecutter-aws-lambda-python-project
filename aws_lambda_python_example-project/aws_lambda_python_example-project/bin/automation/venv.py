# -*- coding: utf-8 -*-

"""
Virtualenv management.
"""

import sys
import shutil
import subprocess

from .pyproject import pyproject
from .paths import (
    dir_venv,
    bin_python,
    bin_pip,
    bin_pytest,
    bin_chalice,
    bin_aws,
    path_poetry_lock,
)
from .runtime import IS_CI
from .helpers import sha256_of_bytes
from .logger import logger
from .emoji import Emoji


@logger.block(
    msg="Try to upload Virtual Environment to cache",
    start_emoji=Emoji.python,
    end_emoji=Emoji.python,
    pipe=Emoji.python,
)
def try_to_upload_venv_cache() -> bool:
    """
    Why caching the Python .venv folder is so hard?

    1. There are lots executable files in the bin folder, if you zip it and unzip
        it in another build, they are not executable by default, you have to use
        ``chmod +x /path/to/bin/script`` to enable it.
    2. A lot bin tool they are not actually binary executable, they are just
        reference to another script. they have shebang ``#!/...`` pointing to
        the path of the real script. However, this is an absolute path and defined
        when the cache was built. It is not compatible on where the cache was used.
    3. There are lots of python library having reference files like
        ``*.pth``, ``*.egg``. For the same reason in #2, it won't work on where
        the cache was used.

    :return: a boolean value to indicate that whether a venv cache is uploaded
    """
    if IS_CI is False:
        return False

    from s3pathlib import S3Path, context
    from boto_session_manager import BotoSesManager

    bsm = BotoSesManager()
    context.attach_boto_session(bsm.boto_ses)

    poetry_lock_hash = sha256_of_bytes(path_poetry_lock.read_bytes())
    s3dir_venv_cache = S3Path.from_s3_uri(
        f"s3://{bsm.aws_account_id}-{bsm.aws_region}-artifacts"
        f"/python_venv_cache/python{sys.version_info.major}.{sys.version_info.minor}/"
    ).to_dir()
    s3path_venv_cache = s3dir_venv_cache.joinpath(f"{poetry_lock_hash}.zip")
    path_venv_cache_zip = dir_venv.parent.joinpath(".venv.zip")

    if s3path_venv_cache.exists() is False:
        shutil.make_archive(
            base_name=f"{dir_venv}",
            format="zip",
            root_dir=f"{dir_venv}",
        )
        s3path_venv_cache.upload_file(f"{path_venv_cache_zip}")
        logger.info(f"{Emoji.green_square} successfully upload venv cache to s3.")
    else:
        logger.info(f"{Emoji.green_square} venv cache already exists, do nothing.")


@logger.block(
    msg="Try to download Virtual Environment cache",
    start_emoji=Emoji.python,
    end_emoji=Emoji.python,
    pipe=Emoji.python,
)
def try_to_download_venv_cache() -> bool:
    """
    :return: a boolean value to indicate that whether a venv cache is downloaded
    """
    if IS_CI is False:
        return False

    from s3pathlib import S3Path, context
    from boto_session_manager import BotoSesManager

    bsm = BotoSesManager()
    context.attach_boto_session(bsm.boto_ses)

    poetry_lock_hash = sha256_of_bytes(path_poetry_lock.read_bytes())
    s3dir_venv_cache = S3Path.from_s3_uri(
        f"s3://{bsm.aws_account_id}-{bsm.aws_region}-artifacts"
        f"/python_venv_cache/python{sys.version_info.major}.{sys.version_info.minor}/"
    ).to_dir()
    s3path_venv_cache = s3dir_venv_cache.joinpath(f"{poetry_lock_hash}.zip")
    path_venv_cache_zip = dir_venv.parent.joinpath(".venv.zip")
    if s3path_venv_cache.exists():
        path_venv_cache_zip.write_bytes(s3path_venv_cache.read_bytes())
        shutil.unpack_archive(
            filename=path_venv_cache_zip,
            extract_dir=dir_venv,
            format="zip",
        )
        for bin_script in [
            bin_python,
            bin_pip,
            bin_pytest,
            bin_chalice,
            bin_aws,
        ]:
            if bin_script.exists():
                args = ["chmod", "+x", f"{bin_script}"]
                subprocess.run(args)
        logger.info(f"{Emoji.green_square} successfully downloaded venv cache from s3.")
        return True
    else:
        logger.info(f"{Emoji.red_circle} s3 venv cache not exists.")
        return False


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
    if dir_venv.exists():
        logger.info(f"{dir_venv} already exists, do nothing.")
    else:
        subprocess.run(
            ["poetry", "config", "virtualenvs.in-project", "true", "--local"],
            check=True,
        )
        subprocess.run(
            ["poetry", "env", "use", f"python{pyproject.python_version}"],
            check=True,
        )
        logger.info("done")


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
    if dir_venv.exists():
        logger.info(f"{dir_venv} already exists, do nothing.")
    else:
        subprocess.run(
            ["virtualenv", "-p", f"python{pyproject.python_version}", f"{dir_venv}"],
            check=True,
        )
        logger.info("done")


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
