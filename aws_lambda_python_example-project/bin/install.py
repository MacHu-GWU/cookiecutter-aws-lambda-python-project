# -*- coding: utf-8 -*-

from automation.runtime import print_runtime_info
from automation.env import print_env_info
from automation.git import print_git_info
from automation.venv import virtualenv_venv_create
from automation.deps import (
    poetry_export,
    pip_install,
    pip_install_dev,
    pip_install_test,
    pip_install_automation,
)


def install():
    print_runtime_info()
    print_env_info()
    print_git_info()
    virtualenv_venv_create()
    poetry_export()
    pip_install()
    pip_install_dev()
    pip_install_test()
    pip_install_automation()


if __name__ == "__main__":
    install()
