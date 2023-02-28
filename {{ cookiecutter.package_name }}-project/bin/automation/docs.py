# -*- coding: utf-8 -*-

import os
import shutil
import subprocess

from .paths import (
    dir_venv,
    dir_venv_bin,
    dir_sphinx_doc,
    dir_sphinx_doc_build,
    dir_sphinx_doc_build_html,
    dir_sphinx_doc_source_python_lib,
)
from .operation_system import OPEN_COMMAND
from .logger import logger
from .emoji import Emoji


@logger.block(
    msg="Build Documentation Site Locally",
    start_emoji=Emoji.doc,
    end_emoji=Emoji.doc,
    pipe=Emoji.doc,
)
def build_doc():
    shutil.rmtree(f"{dir_sphinx_doc_build}", ignore_errors=True)
    shutil.rmtree(f"{dir_sphinx_doc_source_python_lib}", ignore_errors=True)

    # this allows the ``make html`` command knows which python virtualenv to use
    # see more information at: https://docs.python.org/3/library/venv.html
    os.environ["PATH"] = f"{dir_venv_bin}" + os.pathsep + os.environ.get("PATH", "")
    os.environ["VIRTUAL_ENV"] = f"{dir_venv}"
    args = [
        "make",
        "-C",
        f"{dir_sphinx_doc}",
        "html",
    ]
    subprocess.run(args)


def view_doc():
    if dir_sphinx_doc_build_html.joinpath("index.html").exists():
        path_doc_index_html = dir_sphinx_doc_build_html.joinpath("index.html")
    elif dir_sphinx_doc_build_html.joinpath("README.html").exists():
        path_doc_index_html = dir_sphinx_doc_build_html.joinpath("README.html")
    else:
        raise ValueError("documentation index html file not exists!")

    subprocess.call([OPEN_COMMAND, f"{path_doc_index_html}"])
