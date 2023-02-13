# -*- coding: utf-8 -*-

"""
This script can be used for local test.
"""

from automation.deps import poetry_export
from automation.lbd import build_lambda_layer_artifacts

poetry_export()
build_lambda_layer_artifacts()
