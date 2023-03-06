# -*- coding: utf-8 -*-

from chalice import Chalice
from chalice.app import S3Event

from aws_lambda_python_example.config.init import config
from aws_lambda_python_example.iac.output import Output
from aws_lambda_python_example.lbd import hello, s3sync

env = config.env
app = Chalice(app_name=env.chalice_app_name)

stack_output = Output.get()


@app.lambda_function(name=env.func_name_hello)
def hello_lambda_handler(event, context):
    return hello.lambda_handler(event, context)


@app.on_s3_event(
    name=env.func_name_s3sync,
    bucket=config.env.s3dir_source.bucket,
    prefix=config.env.s3dir_source.key,
    events=["s3:ObjectCreated:*"],
)
def s3sync_lambda_handler(event: S3Event):
    return s3sync.lambda_handler(bucket=event.bucket, key=event.key)
