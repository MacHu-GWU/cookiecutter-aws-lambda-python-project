# -*- coding: utf-8 -*-

import typing as T
import attr
import cottonformation as cf
from cottonformation.res import iam

if T.TYPE_CHECKING:
    from .main import Stack


@attr.s
class IamMixin:
    def mk_rg1_iam(self: "Stack"):
        """
        It is very common to declare a group of IAM resources for the project.

        Ref:

        - IAM Object quotas: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entities
        """
        # declare a resource group
        self.rg1_iam = cf.ResourceGroup("rg1_iam")

        # declare policy statements
        stat_parameter_store = {
            "Effect": "Allow",
            "Action": "ssm:GetParameter",
            "Resource": cf.Sub(
                string="arn:aws:ssm:${aws_region}:${aws_account_id}:parameter/${parameter_name}",
                data=dict(
                    aws_region=cf.AWS_REGION,
                    aws_account_id=cf.AWS_ACCOUNT_ID,
                    parameter_name=self.env.parameter_name,
                ),
            ),
        }

        stat_parameter_store = {
            "Effect": "Allow",
            "Action": "ssm:GetParameter",
            "Resource": cf.Sub(
                string="arn:aws:ssm:${aws_region}:${aws_account_id}:parameter/${parameter_name}",
                data=dict(
                    aws_region=cf.AWS_REGION,
                    aws_account_id=cf.AWS_ACCOUNT_ID,
                    parameter_name=self.env.parameter_name,
                ),
            ),
        }

        stat_s3_bucket_read = {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject",
                "s3:GetObjectAttributes",
                "s3:GetObjectTagging",
            ],
            "Resource": [
                f"arn:aws:s3:::{self.env.s3dir_source.bucket}",
                f"arn:aws:s3:::{self.env.s3dir_source.bucket}/{self.env.s3dir_source.key}*",
            ],
        }

        stat_s3_bucket_write = {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:PutObjectTagging",
                "s3:DeleteObjectTagging",
            ],
            "Resource": [
                f"arn:aws:s3:::{self.env.s3dir_target.bucket}",
                f"arn:aws:s3:::{self.env.s3dir_target.bucket}/{self.env.s3dir_target.key}*",
            ],
        }

        # declare iam role
        self.iam_role_for_lambda = iam.Role(
            "IamRoleForLambda",
            rp_AssumeRolePolicyDocument=cf.helpers.iam.AssumeRolePolicyBuilder(
                cf.helpers.iam.ServicePrincipal.awslambda(),
            ).build(),
            p_RoleName=self.env.iam_role_name_lambda,
            p_ManagedPolicyArns=[
                cf.helpers.iam.AwsManagedPolicy.AWSLambdaBasicExecutionRole,
            ],
        )
        self.rg1_iam.add(self.iam_role_for_lambda)

        self.output_iam_role_lambda_arn = cf.Output(
            "IamRoleLambdaArn",
            Value=self.iam_role_for_lambda.rv_Arn,
        )
        self.rg1_iam.add(self.output_iam_role_lambda_arn)

        statement = self.encode_statement(
            [
                stat_parameter_store,
                stat_s3_bucket_read,
                stat_s3_bucket_write,
            ]
        )

        self.iam_inline_policy_for_lambda = iam.Policy(
            "IamInlinePolicyForLambda",
            rp_PolicyName=f"{self.env.prefix_name_snake}-lambda",
            rp_PolicyDocument={"Version": "2012-10-17", "Statement": statement},
            p_Roles=[
                self.iam_role_for_lambda.ref(),
            ],
            ra_DependsOn=self.iam_role_for_lambda,
        )
        self.rg1_iam.add(self.iam_inline_policy_for_lambda)
