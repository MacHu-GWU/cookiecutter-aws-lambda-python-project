# -*- coding: utf-8 -*-

"""
Enum important path on the local file systems for this project.

.. note::

    This module is "ZERO-DEPENDENCY".
"""

import os
import subprocess
import contextlib
from pathlib import Path

from .pyproject import pyproject, path_pyproject_toml

dir_home = Path.home()
dir_project_root = Path(__file__).absolute().parent.parent.parent

assert dir_project_root.joinpath("Makefile").exists() is True

dir_python_lib = dir_project_root / pyproject.package_name
path_version_file = dir_python_lib / "_version.py"

_version = subprocess.run(
    ["python", f"{path_version_file}"],
    capture_output=True,
).stdout.decode("utf-8").strip()
if _version != pyproject.package_version:
    raise ValueError(
        f"The version in {path_version_file} and the version in "
        f"{path_pyproject_toml} doesn't match!"
    )

# ------------------------------------------------------------------------------
# Virtual Environment Related
# ------------------------------------------------------------------------------
dir_venv = dir_project_root / ".venv"
dir_venv_bin = dir_venv / "bin"

# virtualenv executable paths
bin_python = dir_venv_bin / "python"
bin_pip = dir_venv_bin / "pip"
bin_pytest = dir_venv_bin / "pytest"
bin_chalice = dir_venv_bin / "chalice"
bin_aws = dir_venv_bin / "aws"

# ------------------------------------------------------------------------------
# Test Related
# ------------------------------------------------------------------------------
dir_tests = dir_project_root / "tests"
dir_tests_int = dir_project_root / "tests_int"

dir_htmlcov = dir_project_root / "htmlcov"

# ------------------------------------------------------------------------------
# Doc Related
# ------------------------------------------------------------------------------
dir_sphinx_doc = dir_project_root / "docs"
dir_sphinx_doc_source = dir_sphinx_doc / "source"
dir_sphinx_doc_source_conf_py = dir_sphinx_doc_source / "conf.py"
dir_sphinx_doc_source_python_lib = dir_sphinx_doc_source / pyproject.package_name
dir_sphinx_doc_build = dir_sphinx_doc / "build"
dir_sphinx_doc_build_html = dir_sphinx_doc_build / "html"
path_sphinx_doc_build_html_index = dir_sphinx_doc_build_html / "index.html"

# ------------------------------------------------------------------------------
# Poetry Related
# ------------------------------------------------------------------------------
path_requirements_main = dir_project_root / "requirements-main.txt"
path_requirements_dev = dir_project_root / "requirements-dev.txt"
path_requirements_test = dir_project_root / "requirements-test.txt"
path_requirements_doc = dir_project_root / "requirements-doc.txt"
path_requirements_automation = dir_project_root / "requirements-automation.txt"

path_poetry_lock = dir_project_root / "poetry.lock"
path_poetry_lock_hash_json = dir_project_root / ".poetry-lock-hash.json"

# ------------------------------------------------------------------------------
# Env Related
# ------------------------------------------------------------------------------
path_current_env_name_json = dir_project_root / ".current-env-name.json"

# ------------------------------------------------------------------------------
# Config Related
# ------------------------------------------------------------------------------
dir_config = dir_project_root / "config"
path_config_json = dir_config / "config.json"
path_secret_config_json = dir_home / ".projects" / pyproject.package_name / "config-secret.json"

# ------------------------------------------------------------------------------
# CloudFormation Related
# ------------------------------------------------------------------------------
dir_deploy = dir_project_root / "deploy"

# ------------------------------------------------------------------------------
# Build Related
# ------------------------------------------------------------------------------
dir_build = dir_project_root / "build"
dir_dist = dir_project_root / "dist"

# ------------------------------------------------------------------------------
# Lambda Related
# ------------------------------------------------------------------------------
dir_build_lambda = dir_build / "lambda"
dir_build_lambda_python = dir_build_lambda / "python"
path_build_lambda_bin_aws = dir_build_lambda_python / "aws"
path_build_lambda_source_zip = dir_build_lambda / "source.zip"
path_build_lambda_layer_zip = dir_build_lambda / "layer.zip"

dir_lambda_app = dir_project_root / "lambda_app"
path_chalice_config = dir_lambda_app / ".chalice" / "config.json"
dir_lambda_app_vendor = dir_lambda_app / "vendor"
dir_lambda_app_deployed = dir_lambda_app / ".chalice" / "deployed"
path_update_chalice_config_script = dir_lambda_app / "update_chalice_config.py"
path_app_py = dir_lambda_app / "app.py"


@contextlib.contextmanager
def temp_current_dir(path: Path):
    """
    Temporarily set the current directory to target path.
    """
    path = path.absolute()
    if not path.is_dir():
        raise ValueError(f"{path} is not a dir!")

    cwd = os.getcwd()
    os.chdir(f"{path}")
    try:
        yield path
    finally:
        os.chdir(cwd)
