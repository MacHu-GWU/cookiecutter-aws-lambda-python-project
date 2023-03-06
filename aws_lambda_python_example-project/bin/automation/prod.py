# -*- coding: utf-8 -*-

"""
This script can be used to deploy this project from a different git repo.
"""

from .env import EnvEnum, CURRENT_ENV
from .cf import deploy_cloudformation_stack
from .lbd import deploy_lambda_app


def deploy_to_prod():
    if CURRENT_ENV != EnvEnum.prod:
        raise EnvironmentError("It is NOT prod environment, you cannot deploy to prod")
    deploy_cloudformation_stack()
    deploy_lambda_app()
