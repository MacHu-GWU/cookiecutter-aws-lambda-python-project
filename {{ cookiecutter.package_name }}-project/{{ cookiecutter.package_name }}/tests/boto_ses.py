# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager

bsm = BotoSesManager(
    profile_name="{{ cookiecutter.aws_profile }}",
    region_name="{{ cookiecutter.aws_region }}",
)
