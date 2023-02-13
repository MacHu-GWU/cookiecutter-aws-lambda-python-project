# -*- coding: utf-8 -*-

"""
This script should ONLY be run in CI.
"""

from automation.deps import poetry_export
from automation.lbd import (
    IS_LAYER_BRANCH,
    build_lambda_layer_artifacts,
    upload_lambda_layer_artifacts,
    publish_lambda_layer,
)

if IS_LAYER_BRANCH is True:
    poetry_export()

build_lambda_layer_artifacts()
upload_lambda_layer_artifacts()
publish_lambda_layer()
