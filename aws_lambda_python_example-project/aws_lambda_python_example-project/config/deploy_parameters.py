# -*- coding: utf-8 -*-

from aws_lambda_python_example.boto_ses import bsm
from aws_lambda_python_example.config.init import config

config.deploy(bsm=bsm, parameter_with_encryption=True)
# config.delete(bsm=bsm, use_parameter_store=True)