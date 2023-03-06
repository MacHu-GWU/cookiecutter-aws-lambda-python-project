# -*- coding: utf-8 -*-

from pathlib_mate import Path
from .runtime import IS_LOCAL

dir_here = Path.dir_here(__file__)
PACKAGE_NAME = dir_here.basename

dir_project_root = Path.dir_here(__file__).parent
dir_home = Path.home() # ${HOME}
dir_home_project_root = dir_home / ".projects" / PACKAGE_NAME
if IS_LOCAL:
    dir_home_project_root.mkdir_if_not_exists()

# ------------------------------------------------------------------------------
# Config Management Related
# ------------------------------------------------------------------------------
dir_config = dir_project_root / "config"
# where you store the non-sensitive config data
path_config_json = dir_config / "config.json"
# where you store the sensitive config dat
path_config_secret_json = dir_home_project_root / "config-secret.json"
# cache file for current environment name, will only be used in CI
path_current_env_name_json = dir_project_root / ".current-env-name.json"

# ------------------------------------------------------------------------------
# Virtual Environment Related
# ------------------------------------------------------------------------------
dir_venv = dir_project_root / ".venv"
dir_venv_bin = dir_venv / "bin"

# virtualenv executable paths
bin_pytest = dir_venv_bin / "pytest"

# test related
dir_htmlcov = dir_project_root / "htmlcov"
path_cov_index_html = dir_htmlcov / "index.html"
dir_unit_test = dir_project_root / "tests"
dir_int_test = dir_project_root / "tests_int"

# ------------------------------------------------------------------------------
# Lambda App Related
# ------------------------------------------------------------------------------
dir_lambda_app = dir_project_root / "lambda_app"
path_chalice_config = dir_lambda_app / ".chalice" / "config.json"
