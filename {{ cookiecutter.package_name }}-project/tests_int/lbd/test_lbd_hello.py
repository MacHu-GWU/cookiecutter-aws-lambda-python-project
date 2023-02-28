# -*- coding: utf-8 -*-

import pytest
import os
import json
import base64

from aws_console_url import AWSConsole

from {{ cookiecutter.package_name }}.config.init import config
from {{ cookiecutter.package_name }}.boto_ses import bsm
from {{ cookiecutter.package_name }}.logger import logger

aws = AWSConsole(
    aws_account_id=bsm.aws_account_id,
    aws_region=bsm.aws_region,
    bsm=bsm,
)


def _test():
    # test case 1
    payload = {"name": "bob"}
    response = bsm.lambda_client.invoke(
        FunctionName=config.env.func_fullname_hello,
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=json.dumps(payload),
    )
    request_id = response["ResponseMetadata"]["RequestId"]
    logs_console_url = aws.cloudwatch.filter_log_event_by_lambda_request_id(
        func_name=config.env.func_fullname_hello,
        request_id=request_id,
    )
    logger.info(f"preview lambda logs: {logs_console_url}")

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
    request_id = response["ResponseMetadata"]["RequestId"]
    logs_console_url = aws.cloudwatch.filter_log_event_by_lambda_request_id(
        func_name=config.env.func_fullname_hello,
        request_id=request_id,
    )
    logger.info(f"preview lambda logs: {logs_console_url}")
    log = base64.b64decode(response["LogResult"].encode("utf-8")).decode("utf-8")
    result: dict = json.loads(response["Payload"].read().decode("utf-8"))

    # print(log)
    assert result["message"] == "hello Mr X"


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
