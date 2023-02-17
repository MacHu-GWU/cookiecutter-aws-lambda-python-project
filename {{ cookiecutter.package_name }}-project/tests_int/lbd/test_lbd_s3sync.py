# -*- coding: utf-8 -*-

import pytest
import os
import time


from {{ cookiecutter.package_name }}.config.init import config


def test():
    # --------------------------------------------------------------------------
    # before
    # --------------------------------------------------------------------------
    basename = "test.txt"
    s3path_source = config.env.s3dir_source.joinpath(basename)
    s3path_target = config.env.s3dir_target.joinpath(basename)

    s3path_target.delete_if_exists()
    s3path_source.write_text("hello")

    assert s3path_target.exists() is False
    time.sleep(5)

    # --------------------------------------------------------------------------
    # after
    # --------------------------------------------------------------------------
    assert s3path_target.read_text() == "hello"


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
