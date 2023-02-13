# -*- coding: utf-8 -*-

import cottonformation as cf
from aws_idp_doc_store.boto_ses import bsm
from aws_idp_doc_store.iac.define import Stack
from aws_idp_doc_store.config.init import config

env_name = "dev"

env = config.get_env(env_name)

tpl = cf.Template(Description="Application - Documentation Storage")

stack = Stack(env=env)
print(stack.get_output_value(bsm, stack.output_sns_topic_arn.id))
print(stack.get_output_value(bsm, stack.output_iam_role_textract_arn.id))