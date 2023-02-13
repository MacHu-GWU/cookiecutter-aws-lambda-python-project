# -*- coding: utf-8 -*-

from {{ cookiecutter.package_name }}.boto_ses import bsm
from {{ cookiecutter.package_name }}.config.init import config

config.deploy(bsm=bsm, parameter_with_encryption=True)
# config.delete(bsm=bsm, use_parameter_store=True)