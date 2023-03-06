# -*- coding: utf-8 -*-

# helpers
from .logger import logger
from .emoji import Emoji

# actions
from .venv import (
    virtualenv_venv_create,
)
from .deps import (
    poetry_export,
    pip_install,
    pip_install_dev,
    pip_install_test,
    pip_install_automation,
)
from .tests import (
    run_cov_test,
    run_int_test,
)


@logger.block(
    msg="Install Phase",
    start_emoji=f"{Emoji.start} {Emoji.pre_build_phase}",
    end_emoji=Emoji.pre_build_phase,
    pipe=Emoji.pre_build_phase,
)
def install_phase():
    with logger.nested():
        virtualenv_venv_create()
        poetry_export()
        pip_install()
        pip_install_dev()
        pip_install_test()
        pip_install_automation()


@logger.block(
    msg="Pre Build Phase",
    start_emoji=f"{Emoji.start} {Emoji.pre_build_phase}",
    end_emoji=Emoji.pre_build_phase,
    pipe=Emoji.pre_build_phase,
)
def pre_build_phase():
    from .runtime import print_runtime_info
    from .env import print_env_info
    from .git import print_git_info

    print_runtime_info()
    print_env_info()
    print_git_info()

    with logger.nested():
        run_cov_test()


@logger.block(
    msg="Build Phase",
    start_emoji=f"{Emoji.start} {Emoji.build_phase}",
    end_emoji=Emoji.build_phase,
    pipe=Emoji.build_phase,
)
def build_phase():
    from .cf import deploy_cloudformation_stack
    from .lbd import (
        deploy_lambda_layer,
        deploy_lambda_app,
    )

    with logger.nested():
        # CloudFormation
        deploy_cloudformation_stack()

        # Lambda Layer
        deploy_lambda_layer()

        # Deploy Lambda App
        deploy_lambda_app()

        # Run integration test
        run_int_test()


@logger.block(
    msg="Post Phase",
    start_emoji=f"{Emoji.start} {Emoji.post_build_phase}",
    end_emoji=Emoji.post_build_phase,
    pipe=Emoji.post_build_phase,
)
def post_build_phase():
    from .config import backup_prod_config
    from .cf import delete_cloudformation_stack
    from .lbd import delete_lambda_app

    with logger.nested():
        # Backup prod config
        backup_prod_config()

        delete_lambda_app()
        delete_cloudformation_stack()
