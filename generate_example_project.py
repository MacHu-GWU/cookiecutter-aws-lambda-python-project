# -*- coding: utf-8 -*-

"""
I would like to include an example project that is generated from this template.
This script can automatically generate the example project.
"""

import shutil
from pathlib import Path
from cookiecutter.main import cookiecutter


dir_here: Path = Path(__file__).absolute().parent
dir_output = dir_here.joinpath("aws_lambda_python_example-project")

shutil.rmtree(dir_output, ignore_errors=True)
cookiecutter(
    template=f"{dir_here}",
    output_dir=f"{dir_here}",
    extra_context={
        "package_name": "aws_lambda_python_example",
        "author_name": "Firstname Lastname",
        "author_email": "firstname.lastname@email.com",
        "semantic_version": "0.1.1",
        "aws_profile": "my_aws_profile",
        "aws_account_id": "111122223333",
        "aws_region": "us-east-1",
    },
    no_input=True,
)
