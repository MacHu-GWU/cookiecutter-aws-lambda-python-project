# -*- coding: utf-8 -*-

from automation.deps import poetry_export
from automation.lbd import deploy_lambda_app

poetry_export()
deploy_lambda_app()
