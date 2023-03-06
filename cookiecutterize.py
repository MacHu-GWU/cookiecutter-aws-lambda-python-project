# -*- coding: utf-8 -*-

"""
The upstream concrete repo is ``aws_python-project``. This script can convert
the concrete repo into a project template
"""

import shutil
from pathlib import Path
from cookiecutter_maker.maker import Maker

dir_here: Path = Path(__file__).absolute().parent
dir_tmp = dir_here.joinpath("tmp")
if dir_tmp.exists():
    shutil.rmtree(dir_tmp)
dir_tmp.mkdir(parents=True, exist_ok=True)

maker = Maker.new(
    input_dir=Path.home().joinpath("Documents", "CodeCommit", "aws_python-project"),
    output_dir=dir_tmp,
    mapper=[
        ("aws_python", "package_name"),
        ("", "author_name"),
        ("", "author_email"),
        ("", "semantic_version"),
        ("", "aws_profile"),
        ("", "aws_account_id"),
        ("", "aws_region"),
    ],
    include=[],
    exclude=[
        # dir
        ".venv",
        ".pytest_cache",
        ".git",
        ".idea",
        "build",
        "dist",
        "htmlcov",
        "docs/source/aws_python",
        # file
        ".coverage",
        "bin/tests.py",
    ],
    overwrite=True,
    debug=False,
)
maker.templaterize()

dir_before = dir_tmp.joinpath("{{ cookiecutter.package_name }}-project")
dir_after = dir_here.joinpath("{{ cookiecutter.package_name }}-project")
shutil.rmtree(dir_after, ignore_errors=True)
shutil.copytree(dir_before, dir_after)
