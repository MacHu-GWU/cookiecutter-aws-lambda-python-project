# -*- coding: utf-8 -*-

import os
import pytest
from {{ cookiecutter.package_name }}.config.init import config


def test():
    # constant
    _ = config

    _ = config.env

    # constant attributes
    _ = config.env.username
    _ = config.env.password
    _ = config.env.s3uri_source
    _ = config.env.s3uri_target

    # derived attributes
    _ = config.env.s3dir_source
    _ = config.env.s3dir_target


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
