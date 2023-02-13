# -*- coding: utf-8 -*-

from automation.deps import poetry_export
from automation.lbd import delete_lambda_app

poetry_export()
delete_lambda_app()
