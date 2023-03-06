# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager

bsm = BotoSesManager(
    profile_name="my_aws_profile",
    region_name="us-east-1",
)
