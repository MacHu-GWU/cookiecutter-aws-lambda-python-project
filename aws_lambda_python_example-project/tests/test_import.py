# -*- coding: utf-8 -*-

import os
import pytest
import aws_lambda_python_example


def test_import():
    _ = aws_lambda_python_example


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
