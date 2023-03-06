# -*- coding: utf-8 -*-

import typing as T
import dataclasses
import os
import json

from config_patterns.patterns.multi_env_json import (
    BaseEnvEnum,
    BaseEnv,
    BaseConfig,
)
from s3pathlib import S3Path

from ...runtime import IS_LOCAL, IS_CI, IS_LAMBDA
from ...paths import path_current_env_name_json
from ...compat import cached_property


class EnvEnum(BaseEnvEnum):
    """
    In this project, we have three environment:

    - dev: represent the developer's local laptop. the change you made on your
        local laptop can be applied to dev.
    - int: a long living integration test environment. once the development work
        been merged to main branch, it will be deployed to int for QA.
    - prod: the production environment. can only be deployed from release branch.
    """
    dev = "dev"
    int = "int"
    prod = "prod"


# You may have a long list of config field definition
# put them in different module and use Mixin class
from .app import AppMixin
from .name import NameMixin
from .deploy import DeployMixin
from .cloudformation import CloudFormationMixin
from .lbd_deploy import LambdaDeployMixin
from .lbd_func import LambdaFunctionMixin


@dataclasses.dataclass
class Env(
    BaseEnv,
    AppMixin,
    NameMixin,
    DeployMixin,
    CloudFormationMixin,
    LambdaDeployMixin,
    LambdaFunctionMixin,
):
    pass


class Config(BaseConfig):
    @classmethod
    def get_current_env(cls) -> str:
        # you can uncomment this line to force to use certain env
        # from your local laptop to run application code, tests, ...
        # return EnvEnum.dev.value
        if IS_LOCAL:
            return EnvEnum.dev.value
        elif IS_CI:
            # the automation script for CI will detect the env it
            # should deal with and write to this cache file.
            # so you just need to read from it in your application code.
            return json.loads(
                path_current_env_name_json.read_text()
            )["env"]
        elif IS_LAMBDA:
            return os.environ["ENV_NAME"]

    @cached_property
    def dev(self) -> Env:
        return self.get_env(env_name=EnvEnum.dev)

    @cached_property
    def int(self) -> Env:
        return self.get_env(env_name=EnvEnum.int)

    @cached_property
    def prod(self) -> Env:
        return self.get_env(env_name=EnvEnum.prod)

    @cached_property
    def env(self) -> Env:
        return self.get_env(env_name=self.get_current_env())
