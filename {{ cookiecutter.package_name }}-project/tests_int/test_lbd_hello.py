# -*- coding: utf-8 -*-

import pytest
import os
import json
import base64

from {{ cookiecutter.package_name }}.config.init import config
from {{ cookiecutter.package_name }}.boto_ses import bsm


def test():
    # test case 1
    payload = {"name": "bob"}
    response = bsm.lambda_client.invoke(
        FunctionName=config.env.func_fullname_hello,
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=json.dumps(payload),
    )
    log = base64.b64decode(response["LogResult"].encode("utf-8")).decode("utf-8")
    result: dict = json.loads(response["Payload"].read().decode("utf-8"))

    # print(log)
    assert result["message"] == "hello bob"

    # test case 2
    payload = {}
    response = bsm.lambda_client.invoke(
        FunctionName=config.env.func_fullname_hello,
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=json.dumps(payload),
    )
    log = base64.b64decode(response["LogResult"].encode("utf-8")).decode("utf-8")
    result: dict = json.loads(response["Payload"].read().decode("utf-8"))

    # print(log)
    assert result["message"] == "hello Mr X"


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
