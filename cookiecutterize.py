# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
from cookiecutter_maker.maker import Maker

dir_tmp: Path = Path(__file__).absolute().parent.joinpath("tmp")
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
