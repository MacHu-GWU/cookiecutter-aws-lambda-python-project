# -*- coding: utf-8 -*-

from rich.table import Table
from rich.text import Text
from rich.style import Style

from .logger import console
from .paths import (
    dir_project_root,
    dir_python_lib,
    dir_venv,
    bin_python,
    path_config_json,
    path_secret_config_json,
)


def show_path(name, path):
    console.print("| | ", Text(name, style="green"), Text(str(path), style="red"))


def _file(title, path) -> tuple:
    return (
        Text(str(title), style=Style(link=f"file://{path}")),
        Text(str(path), style=Style(link=f"file://{path}")),
    )


def _s3path(title, s3path) -> tuple:
    return (
        Text(title, style=Style(link=s3path.console_url)),
        # Text(s3path.uri, style=Style(link=s3path.console_url)),
        Text(s3path.console_url, style=Style(link=s3path.console_url)),
    )


def _url(title, url) -> tuple:
    return (
        Text(title, style=Style(link=url)),
        Text(url, style=Style(link=url)),
    )


def show_important_paths():
    table = Table(title="Important Local Paths")

    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("Path", no_wrap=True)

    table.add_row(*_file("dir_project_root", dir_project_root))
    table.add_row(*_file("dir_python_lib", dir_python_lib))
    table.add_row(*_file("dir_venv", dir_venv))
    table.add_row(*_file("bin_python", bin_python))
    table.add_row(*_file("path_config_json", path_config_json))
    table.add_row(*_file("path_secret_config_json", path_secret_config_json))

    console.print(table)


def show_important_s3_location():
    from {{ cookiecutter.package_name }}.config.init import config

    table = Table(title="Important S3 Location")

    table.add_column("Title", style="cyan", no_wrap=True)
    # table.add_column("S3 Uri", no_wrap=True)
    table.add_column("S3 Console", no_wrap=True)

    table.add_row(*_s3path("s3dir_artifacts", config.env.s3dir_artifacts))
    table.add_row(
        *_s3path(
            "s3dir_cloudformation_templates", config.env.s3dir_cloudformation_templates
        )
    )
    table.add_row(*_s3path("s3dir_config", config.env.s3dir_config))
    table.add_row(*_s3path("s3dir_lambda_layer", config.env.s3dir_lambda_layer))
    table.add_row(*_s3path("s3dir_lambda_source", config.env.s3dir_lambda_source))
    table.add_row(*_s3path("s3dir_deployed_lambda", config.env.s3dir_deployed))

    console.print(table)


def show_important_aws_console_url():
    from aws_console_url import AWSConsole

    from {{ cookiecutter.package_name }}.config.init import config
    from {{ cookiecutter.package_name }}.boto_ses import bsm

    aws = AWSConsole(
        aws_account_id=bsm.aws_account_id,
        aws_region=bsm.aws_region,
        bsm=bsm,
    )

    table = Table(title="Important AWS Console Url")

    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("Url", no_wrap=True)

    table.add_row(*_url("codecommit", aws.codecommit.repositories))
    table.add_row(*_url("codebuild", aws.codebuild.build_projects))
    table.add_row(
        *_url("parameter store", aws.ssm.filter_parameters(config.parameter_name))
    )
    table.add_row(*_url("cloudformation stacks", aws.cloudformation.stacks))
    table.add_row(
        *_url(
            "lambda functions",
            aws.awslambda.filter_functions(config.env.chalice_app_name),
        )
    )
    table.add_row(
        *_url("lambda layer", aws.awslambda.get_layer(config.env.lambda_layer_name))
    )

    console.print(table)


def show_project_info():
    show_important_paths()

    try:
        show_important_s3_location()
    except ImportError:
        pass

    try:
        show_important_aws_console_url()
    except ImportError:
        pass
