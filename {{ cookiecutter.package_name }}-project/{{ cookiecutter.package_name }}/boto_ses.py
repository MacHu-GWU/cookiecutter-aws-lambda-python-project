# -*- coding: utf-8 -*-

import pynamodb_mate as pm
from s3pathlib import context
from boto_session_manager import BotoSesManager

from .runtime import IS_LOCAL, IS_CI, IS_LAMBDA

# environment aware boto session manager
if IS_LAMBDA:  # put production first
    bsm = BotoSesManager(
        region_name="{{ cookiecutter.aws_region }}",
    )
elif IS_LOCAL:
    bsm = BotoSesManager(
        profile_name="{{ cookiecutter.aws_profile }}",
        region_name="{{ cookiecutter.aws_region }}",
    )
elif IS_CI:
    bsm = BotoSesManager(
        region_name="{{ cookiecutter.aws_region }}",
    )
else:  # pragma: no cover
    raise NotImplementedError

# Set default s3pathlib boto session
context.attach_boto_session(boto_ses=bsm.boto_ses)

# Set default pynamodb boto session
with bsm.awscli():
    pynamodb_connection = pm.Connection()
