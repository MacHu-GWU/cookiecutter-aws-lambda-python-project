# -*- coding: utf-8 -*-

import os
from config_patterns.jsonutils import json_loads

from ..paths import path_config_json, path_config_secret_json
from ..runtime import IS_LOCAL, IS_CI, IS_LAMBDA
from ..boto_ses import bsm

from .define import EnvEnum, Env, Config

if IS_LOCAL:
    # read non-sensitive config and sensitive config from local file system
    config = Config.read(
        env_class=Env,
        env_enum_class=EnvEnum,
        path_config=path_config_json.abspath,
        path_secret_config=path_config_secret_json.abspath,
    )
elif IS_CI:
    # read non-sensitive config from local file system
    # and then figure out what is the parameter name
    config = Config(
        data=json_loads(path_config_json.read_text()),
        secret_data=dict(),
        Env=Env,
        EnvEnum=EnvEnum,
    )
    # read config from parameter store
    # we consider the value in parameter store is the ground truth for production
    config = Config.read(
        env_class=Env,
        env_enum_class=EnvEnum,
        bsm=bsm,
        parameter_name=config.parameter_name,
        parameter_with_encryption=True,
    )
elif IS_LAMBDA:
    # read the parameter name from environment variable
    parameter_name = os.environ["PARAMETER_NAME"]
    # read config from parameter store
    config = Config.read(
        env_class=Env,
        env_enum_class=EnvEnum,
        bsm=bsm,
        parameter_name=parameter_name,
        parameter_with_encryption=True,
    )
else:
    raise NotImplementedError
