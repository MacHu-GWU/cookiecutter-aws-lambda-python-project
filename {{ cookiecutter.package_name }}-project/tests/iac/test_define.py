# # -*- coding: utf-8 -*-

from {{ cookiecutter.package_name }}.config.define import EnvEnum
from {{ cookiecutter.package_name }}.iac.deploy import deploy_cloudformation_stack


def test():
    deploy_cloudformation_stack(env_name=EnvEnum.dev.name, dry_run=True)


if __name__ == "__main__":
    from {{ cookiecutter.package_name }}.tests import run_cov_test

    run_cov_test(__file__, module="{{ cookiecutter.package_name }}.iac.define", preview=False)
