# # -*- coding: utf-8 -*-

from aws_lambda_python_example.config.define import EnvEnum
from aws_lambda_python_example.iac.deploy import deploy_cloudformation_stack


def test():
    deploy_cloudformation_stack(env_name=EnvEnum.dev.name, dry_run=True)


if __name__ == "__main__":
    from aws_lambda_python_example.tests import run_cov_test

    run_cov_test(__file__, module="aws_lambda_python_example.iac.define", preview=False)
