# -*- coding: utf-8 -*-

import pytest
import os
import time

from {{ cookiecutter.package_name }}.config.init import config
from {{ cookiecutter.package_name }}.logger import logger


def _test():
    # --------------------------------------------------------------------------
    # before
    # --------------------------------------------------------------------------
    basename = "test.txt"
    s3path_source = config.env.s3dir_source.joinpath(basename)
    s3path_target = config.env.s3dir_target.joinpath(basename)

    logger.info(f"preview s3 source: {s3path_source.console_url}")
    logger.info(f"preview s3 target: {s3path_source.console_url}")

    s3path_target.delete_if_exists()
    s3path_source.write_text("hello")

    assert s3path_target.exists() is False
    time.sleep(5)

    # --------------------------------------------------------------------------
    # after
    # --------------------------------------------------------------------------
    assert s3path_target.read_text() == "hello"


def test():
    print("")
    with logger.disabled(
        disable=True,
        # disable=False,
    ):
        _test()


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
