# -*- coding: utf-8 -*-

"""
Update chalice config file based on project config management system.

We have our own project level configuration, and we don't want to manually
copy and paste data to chalice config. We create this script to automatically
sync the project config to the chalice config. Because our project is not only
about Lambda Function.

.. note::

    The chalice config file should not include any sensitive data. If you need
    to access sensitive data from lambda function, please use parameter store.
"""

import json
from {{ cookiecutter.package_name }}._version import __version__
from {{ cookiecutter.package_name }}.paths import path_chalice_config
from {{ cookiecutter.package_name }}.config.init import config
from {{ cookiecutter.package_name }}.config.define import EnvEnum
from {{ cookiecutter.package_name }}.iac.output import StackDoesntExist, Output

stages = dict()

current_env = config.get_current_env()

lambda_functions = {
    config.env.func_name_hello: {
        "lambda_memory_size": 128,
        "lambda_timeout": 3,
    },
    config.env.func_name_s3sync: {
        "lambda_memory_size": 128,
        "lambda_timeout": 30,
    },
}

try:
    output = Output.get(EnvEnum.dev)
    stages[EnvEnum.dev] = {
        "iam_role_arn": output.iam_role_lambda_arn,
        "manage_iam_role": False,
        "layers": [
            "arn:aws:lambda:{{ cookiecutter.aws_region }}:{{ cookiecutter.aws_account_id }}:layer:{{ cookiecutter.package_name }}:1",
        ],
        "environment_variables": {
            "PARAMETER_NAME": config.dev.parameter_name,
            "PROJECT_NAME": config.dev.project_name,
            "ENV_NAME": config.dev.env_name,
            "PACKAGE_VERSION": __version__,
        },
        "tags": {
            "ProjectName": config.dev.project_name,
            "EnvName": config.dev.env_name,
            "PackageVersion": __version__,
        },
        "lambda_functions": lambda_functions,
    }
except StackDoesntExist:
    pass


try:
    output = Output.get(EnvEnum.int)
    stages[EnvEnum.int] = {
        "iam_role_arn": output.iam_role_lambda_arn,
        "manage_iam_role": False,
        "layers": [
            "arn:aws:lambda:{{ cookiecutter.aws_region }}:{{ cookiecutter.aws_account_id }}:layer:{{ cookiecutter.package_name }}:1",
        ],
        "environment_variables": {
            "PARAMETER_NAME": config.int.parameter_name,
            "PROJECT_NAME": config.int.project_name,
            "ENV_NAME": config.int.env_name,
            "PACKAGE_VERSION": __version__,
        },
        "tags": {
            "ProjectName": config.int.project_name,
            "EnvName": config.int.env_name,
            "PackageVersion": __version__,
        },
        "lambda_functions": lambda_functions,
    }
except StackDoesntExist:
    pass


try:
    output = Output.get(EnvEnum.prod)
    stages[EnvEnum.prod] = {
        "iam_role_arn": output.iam_role_lambda_arn,
        "manage_iam_role": False,
        "layers": [
            "arn:aws:lambda:{{ cookiecutter.aws_region }}:{{ cookiecutter.aws_account_id }}:layer:{{ cookiecutter.package_name }}:1",
        ],
        "environment_variables": {
            "PARAMETER_NAME": config.prod.parameter_name,
            "PROJECT_NAME": config.prod.project_name,
            "ENV_NAME": config.prod.env_name,
            "PACKAGE_VERSION": __version__,
        },
        "tags": {
            "ProjectName": config.prod.project_name,
            "EnvName": config.prod.env_name,
            "PackageVersion": __version__,
        },
        "lambda_functions": lambda_functions,
    }
except StackDoesntExist:
    pass


chalice_config_json_data = {
    "version": "2.0",
    "app_name": config.env.chalice_app_name,
    "stages": stages,
}

path_chalice_config.write_text(json.dumps(chalice_config_json_data, indent=4))
