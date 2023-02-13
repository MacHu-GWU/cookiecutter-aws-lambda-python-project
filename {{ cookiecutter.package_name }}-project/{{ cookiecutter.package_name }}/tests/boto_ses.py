# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager, AwsServiceEnum

aws_profile = "aws_data_lab_sanhe_us_east_1"

bsm = BotoSesManager(profile_name=aws_profile)
cf_client = bsm.get_client(AwsServiceEnum.CloudFormation)
