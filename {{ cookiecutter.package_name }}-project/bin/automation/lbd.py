# -*- coding: utf-8 -*-

"""
AWS Lambda Function related automation script.

.. note::

    All of the deployment automation function should have a required parameter
    ``env_name``. We need to ensure developer explicitly know what env they
    are dealing with
"""

import typing as T
import os
import glob
import shutil
import subprocess
from pathlib import Path
from s3pathlib import S3Path

from aws_codecommit import better_boto

from {{ cookiecutter.package_name }} import __version__
from {{ cookiecutter.package_name }}.config.init import config
from {{ cookiecutter.package_name }}.boto_ses import bsm

from .paths import (
    bin_python,
    bin_pip,
    bin_chalice,
    dir_project_root,
    dir_python_lib,
    dir_build_lambda,
    dir_build_lambda_python,
    path_build_lambda_layer_zip,
    dir_lambda_app,
    dir_lambda_app_vendor,
    dir_lambda_app_deployed,
    path_app_py,
    path_chalice_config,
    path_update_chalice_config_script,
    path_requirements_main,
    dir_dist,
    temp_current_dir,
)
from .pyproject import pyproject
from .runtime import IS_CI
from .git import (
    GIT_BRANCH_NAME,
    IS_LAYER_BRANCH,
    IS_LAMBDA_BRANCH,
    IS_INT_BRANCH,
    IS_RELEASE_BRANCH,
    IS_CLEAN_UP_BRANCH,
    COMMIT_MESSAGE_HAS_LBD,
)
from .env import CURRENT_ENV
from .logger import logger
from .emoji import Emoji
from .helpers import sha256_of_bytes
from .deps import _try_poetry_export
from .lbd_rule import (
    do_we_build_lambda_layer as _do_we_build_lambda_layer,
    do_we_publish_lambda_layer,
    do_we_deploy_lambda as _do_we_deploy_lambda,
    do_we_delete_lambda,
)


# ------------------------------------------------------------------------------
# Lambda layer related
# ------------------------------------------------------------------------------
def get_latest_lambda_layer_version() -> T.Optional[int]:
    """
    Call AWS Lambda Layer API, get the latest deployed layer version.

    If returns None, it means no layer deployed yet.

    Ref:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_layer_versions
    """
    res = bsm.lambda_client.list_layer_versions(
        LayerName=config.env.lambda_layer_name,
    )
    if len(res.get("LayerVersions", [])):
        return res["LayerVersions"][0]["Version"]
    else:
        return None


def is_current_layer_the_same_as_latest_one() -> bool:
    """
    Compare the local version of the requirements and the S3 backup of the
    latest layer requirements.
    """
    # check if there is a lambda layer exists
    latest_layer_version = get_latest_lambda_layer_version()
    if latest_layer_version is None:
        return False

    # get the s3 backup of the latest layer requirements
    s3path_lambda_layer_requirements_txt = (
        config.env.get_s3path_lambda_layer_requirements_txt(
            version=latest_layer_version
        )
    )

    # compare
    return (
        path_requirements_main.read_text()
        == s3path_lambda_layer_requirements_txt.read_text()
    )


def do_we_build_lambda_layer() -> bool:
    if (
        _do_we_build_lambda_layer(
            is_ci_runtime=IS_CI,
            branch_name=GIT_BRANCH_NAME,
            is_layer_branch=IS_LAYER_BRANCH,
        )
        is False
    ):
        return False

    if is_current_layer_the_same_as_latest_one():
        logger.info(
            f"{Emoji.red_circle} don't publish layer, "
            f"the current requirements-main.txt is the same as the one "
            f"for the latest lambda layer."
        )
        return False
    else:
        return True


@logger.block(
    msg="Build Lambda Layer Artifacts",
    start_emoji=f"{Emoji.build} {Emoji.awslambda}",
    end_emoji=Emoji.build,
    pipe=Emoji.awslambda,
)
def build_lambda_layer_artifacts():
    """
    This function should only run in CI environment. If you build layer
    on Mac, some C library may not work in AWS Lambda, which is an
    Amazon Linux based container.
    """
    _try_poetry_export()

    # remove existing artifacts and temp folder
    path_build_lambda_layer_zip.unlink(missing_ok=True)
    shutil.rmtree(f"{dir_build_lambda_python}", ignore_errors=True)

    # initialize the build/lambda folder
    dir_build_lambda.mkdir(parents=True, exist_ok=True)

    # do "pip install -r requirements-main.txt -t ./build/lambda/python"
    logger.info("do 'pip install -r requirements-main.txt' ...")
    args = [
        bin_pip,
        "install",
        "-r",
        f"{path_requirements_main}",
        "-t",
        f"{dir_build_lambda_python}",
    ]
    # if IS_CI:
    args.append("--quiet")
    subprocess.run(
        args,
        check=True,
    )

    # zip the layer file
    cwd = os.getcwd()
    os.chdir(dir_build_lambda)
    ignore_package_list = [
        "boto3",
        "botocore",
        "s3transfer",
        "setuptools",
        "pip",
        "wheel",
        "twine",
        "_pytest",
        "pytest",
    ]
    args = (
        [
            "zip",
            f"{path_build_lambda_layer_zip}",
            "-r",
            "-9",
            "-q",
        ]
        + glob.glob("*")
        + [
            "-x",
        ]
    )
    for package in ignore_package_list:
        args.append(f"python/{package}*")
    try:
        subprocess.run(args, check=True)
    except Exception as e:
        os.chdir(cwd)  # ensure to change current dir back and then raise error
        raise e

    logger.info("done!", indent=2)


@logger.block(
    msg="Upload Lambda Layer Artifacts",
    start_emoji=f"{Emoji.deploy} {Emoji.awslambda}",
    end_emoji=Emoji.deploy,
    pipe=Emoji.awslambda,
)
def upload_lambda_layer_artifacts():
    """
    Upload recently built lambda layer artifact to S3 temp folder first.
    If we successfully published a new layer from temp, then copy it to the
    target location.
    """
    s3dir_tmp_lambda_layer_zip = config.env.s3dir_tmp_lambda_layer_zip
    s3dir_tmp_lambda_layer_requirements_txt = (
        config.env.s3dir_tmp_lambda_layer_requirements_txt
    )
    logger.info(f"upload layer.zip to {s3dir_tmp_lambda_layer_zip.uri}")
    logger.info(f"preview at {s3dir_tmp_lambda_layer_zip.console_url}", indent=1)
    logger.info(
        f"preview at {s3dir_tmp_lambda_layer_requirements_txt.console_url}",
        indent=1,
    )

    s3dir_tmp_lambda_layer_zip.upload_file(
        f"{path_build_lambda_layer_zip}",
        overwrite=True,
    )
    s3dir_tmp_lambda_layer_requirements_txt.upload_file(
        f"{path_requirements_main}",
        overwrite=True,
    )
    logger.info("done!", indent=1)


@logger.block(
    msg="Publish a New Lambda Layer",
    start_emoji=f"{Emoji.package} {Emoji.awslambda}",
    end_emoji=Emoji.package,
    pipe=Emoji.awslambda,
)
def publish_lambda_layer() -> T.Optional[str]:
    """
    Publish a new lambda layer version from AWS S3.

    :return: The published lambda layer version ARN
    """
    layer_console_url = (
        f"https://{bsm.aws_region}.console.aws.amazon.com/lambda"
        f"/home?region={bsm.aws_region}#"
        f"/layers?fo=and&o0=%3A&v0={config.env.lambda_layer_name}"
    )

    # publish new layer from temp s3 location first
    s3dir_tmp_lambda_layer_zip = config.env.s3dir_tmp_lambda_layer_zip
    s3dir_tmp_lambda_layer_requirements_txt = (
        config.env.s3dir_tmp_lambda_layer_requirements_txt
    )

    # publish new layer version from temp s3 location
    logger.info(f"preview deployed layer at {layer_console_url}")
    response = bsm.lambda_client.publish_layer_version(
        LayerName=config.env.lambda_layer_name,
        Content=dict(
            S3Bucket=s3dir_tmp_lambda_layer_zip.bucket,
            S3Key=s3dir_tmp_lambda_layer_zip.key,
        ),
        CompatibleRuntimes=[
            f"python{pyproject.python_version}",
        ],
    )
    layer_version_arn = response["LayerVersionArn"]
    layer_version = int(layer_version_arn.split(":")[-1])

    # if success, we copy artifacts from temp to the right location
    s3path_lambda_layer_zip = config.env.get_s3path_lambda_layer_zip(
        version=layer_version
    )
    s3path_lambda_layer_requirements_txt = (
        config.env.get_s3path_lambda_layer_requirements_txt(version=layer_version)
    )
    logger.info(f"preview layer.zip at {s3path_lambda_layer_zip.console_url}")
    logger.info(
        f"preview requirements.txt at {s3path_lambda_layer_requirements_txt.console_url}",
    )
    s3dir_tmp_lambda_layer_zip.copy_to(
        s3path_lambda_layer_zip,
        overwrite=False,  # we don't overwrite existing layer artifacts
    )
    s3dir_tmp_lambda_layer_requirements_txt.copy_to(
        s3path_lambda_layer_requirements_txt,
        overwrite=False,
    )
    logger.info("done!")

    # in CI, post the published Lambda Layer console url to the PR comment if possible
    if IS_CI:
        comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
        if comment_id:
            content = "\n".join(
                [
                    f"{Emoji.succeeded} {Emoji.package} **Published a new Lambda Layer version**",
                    f"",
                    f"- **layer version**: {layer_version}",
                    f"- **layer arn**: ``{layer_version_arn}``",
                    f"- review [Lambda Layer]({layer_console_url})",
                    f"- review [layer zip file]({s3path_lambda_layer_zip.console_url})",
                    f"- review [requirements file]({s3path_lambda_layer_requirements_txt.console_url})",
                ]
            )
            better_boto.post_comment_reply(
                bsm=bsm,
                in_reply_to=comment_id,
                content=content,
            )
    return layer_version_arn


@logger.block(
    msg="Deploy a New Lambda Layer",
    start_emoji=f"{Emoji.package} {Emoji.awslambda}",
    end_emoji=Emoji.package,
    pipe=Emoji.awslambda,
)
def deploy_lambda_layer():
    try:
        if do_we_build_lambda_layer():
            build_lambda_layer_artifacts()
        else:
            return

        if do_we_publish_lambda_layer(
            is_ci_runtime=IS_CI,
            branch_name=GIT_BRANCH_NAME,
            is_layer_branch=IS_LAYER_BRANCH,
        ):
            upload_lambda_layer_artifacts()
            publish_lambda_layer()
            logger.info(f"{Emoji.succeeded} Deploy Lambda layer succeeded!")
        else:
            return
    except Exception as e:
        logger.error(f"{Emoji.failed} Deploy Lambda layer failed!")
        # in CI, post the error message to the PR comment if possible
        if IS_CI:
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                content = "\n".join(
                    [
                        f"{Emoji.failed} Deploy Lambda layer failed!",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
        raise e


# ------------------------------------------------------------------------------
# Lambda Function related
# ------------------------------------------------------------------------------
def run_update_chalice_config_script():
    """
    cmd: ``./.venv/bin/python lambda_app/update_chalice_config.py``
    """
    args = [
        f"{bin_python}",
        f"{path_update_chalice_config_script}",
    ]
    subprocess.run(args, check=True)


def get_lambda_function_hash() -> str:
    """
    Scan lambda related source code, calculate the lambda code hash.

    :return: a sha256 hash value represent the local lambda source code
    """
    # python library
    hashes = list()
    for path in sorted(dir_python_lib.glob("**/*.py"), key=lambda x: str(x)):
        hashes.append(sha256_of_bytes(path.read_bytes()))
    # the app.py
    hashes.append(sha256_of_bytes(path_app_py.read_bytes()))
    # the config.json
    hashes.append(sha256_of_bytes(path_chalice_config.read_bytes()))
    return sha256_of_bytes("".join(hashes).encode("utf-8"))


def is_current_lambda_the_same_as_deployed_one(lambda_function_hash: str) -> bool:
    """
    Compare the local version of the requirements and the S3 backup of the
    latest layer requirements.

    :param lambda_function_hash: a sha256 hash value represent the local lambda source code
    """
    s3path_deployed_json = config.env.get_s3path_deployed_json(CURRENT_ENV)
    if s3path_deployed_json.exists():
        return (
            lambda_function_hash
            == s3path_deployed_json.metadata["lambda_function_hash"]
        )
    else:
        return False


def do_we_deploy_lambda_based_on_hash(lambda_function_hash: str) -> bool:
    """
    :param lambda_function_hash: a sha256 hash value represent the local lambda source code
    """
    if is_current_lambda_the_same_as_deployed_one(lambda_function_hash):
        logger.info(
            f"{Emoji.red_circle} don't deploy lambda app, "
            f"the local lambda source code is the same as the deployed one.",
        )
        return False
    else:
        return True


@logger.block(
    msg="Build Lambda Source Artifacts",
    start_emoji=f"{Emoji.build} {Emoji.awslambda}",
    end_emoji=Emoji.build,
    pipe=Emoji.awslambda,
)
def build_lambda_source_artifacts():
    logger.info("build lambda source artifacts ...")
    shutil.rmtree(f"{dir_dist}", ignore_errors=True)
    _try_poetry_export()
    with temp_current_dir(dir_project_root):
        # option 1: use setup.py,
        # I have more control with python setup.py build
        # subprocess.run(
        #     [
        #         f"{bin_python}",
        #         "setup.py",
        #         "--quiet",
        #         "sdist",
        #         "bdist_wheel",
        #         "--universal",
        #     ],
        #     check=True,
        # )

        # option 2: use ``poetry build``
        # poetry build has a bug that has wrong created date for PKG_INFO file
        subprocess.run(["poetry", "build"], check=True)
    logger.info("done", indent=1)


def download_deployed_json(env_name: str) -> bool:
    """
    AWS Chalice use JSON file to store the deployed resource information.
    We use S3 to store this JSON file.

    :return: a boolean flag to indicate that if the deployed JSON exists on S3
    """
    logger.info(f"download existing deployed {env_name}.json file")
    path_deployed_json = dir_lambda_app_deployed / f"{env_name}.json"
    s3path_deployed_json = config.env.s3dir_deployed / f"{env_name}.json"

    # pull the existing deployed json file from s3
    if s3path_deployed_json.exists():
        logger.info(
            f"preview deployed JSON file at: {s3path_deployed_json.s3_select_console_url}",
            indent=1,
        )
        dir_lambda_app_deployed.mkdir(parents=True, exist_ok=True)
        path_deployed_json.write_text(s3path_deployed_json.read_text())
        return True
    else:
        logger.info("no existing deployed json file found, skip download", indent=1)
        return False


def upload_deployed_json(
    env_name: str,
    lambda_function_hash: str,
) -> S3Path:
    """
    After ``chalice deploy`` succeeded, upload the ``.chalice/deployed/${env_name}.json``
    file from local to s3. It will generate two files:

    1. ``${s3dir_artifacts}/lambda/deployed/${env_name}.json``, this file will
        be overwritten over the time.
    2. ``${s3dir_artifacts}/lambda/deployed/${env_name}-${datetime}.json``, this
        file will stay forever as a backup

    :param env_name: which environment you are dealing with
    :param lambda_function_hash: a sha256 hash value represent the local lambda source code
    """
    logger.info(f"upload the deployed {env_name}.json file")
    path_deployed_json = dir_lambda_app_deployed / f"{env_name}.json"
    s3path_deployed_json = config.env.get_s3path_deployed_json(env_name)
    s3path_deployed_json_backup = config.env.get_s3path_deployed_json_backup(
        CURRENT_ENV
    )

    if path_deployed_json.exists():
        logger.info(
            f"preview deployed JSON file at: {s3path_deployed_json.s3_select_console_url}",
            indent=2,
        )
        content = path_deployed_json.read_text()
        s3path_deployed_json.write_text(
            content,
            metadata={"lambda_function_hash": lambda_function_hash},
            tags={
                "ProjectName": config.project_name,
                "EnvName": env_name,
                "PackageVersion": f"v{pyproject.package_version}",
            },
        )
        s3path_deployed_json_backup.write_text(
            content,
            metadata={"lambda_function_hash": lambda_function_hash},
            tags={
                "ProjectName": config.project_name,
                "EnvName": env_name,
                "PackageVersion": f"{pyproject.package_version}",
            },
        )
    else:
        logger.error("no existing deployed json file found, skip upload", indent=1)
    return s3path_deployed_json


@logger.block(
    msg="Run Chalice Deploy",
    start_emoji=f"{Emoji.deploy} {Emoji.awslambda}",
    end_emoji=Emoji.deploy,
    pipe=Emoji.awslambda,
)
def run_chalice_deploy(
    env_name: str,
    lambda_function_hash: str,
):
    """
    Deploy lambda app using chalice.

    :param lambda_function_hash: a sha256 hash value represent the local lambda source code
    """
    path_tar: T.Optional[Path] = None
    for p in dir_dist.iterdir():
        if p.name.endswith(".tar.gz"):
            path_tar = p
    if path_tar is None:
        raise FileNotFoundError

    s3dir_lambda_source = config.env.get_s3dir_lambda_source(__version__)
    logger.info(f"upload source artifacts to {s3dir_lambda_source.uri}")
    logger.info(f"preview at: {s3dir_lambda_source.console_url}", indent=1)
    s3dir_lambda_source.upload_dir(
        local_dir=f"{dir_dist}",
        overwrite=True,
    )

    # extract .tar.gz file
    logger.info("move source artifacts to vendor folder")
    extracted_folder_name = path_tar.name.replace(".tar.gz", "")
    dir_extracted_folder = dir_lambda_app / extracted_folder_name
    shutil.rmtree(dir_extracted_folder, ignore_errors=True)
    subprocess.run(
        [
            "tar",
            "-xzf",
            f"{path_tar}",
            "-C",
            f"{dir_lambda_app}",
        ],
        check=True,
    )

    # move source code to vendor
    shutil.rmtree(f"{dir_lambda_app_vendor}", ignore_errors=True)
    dir_lambda_app_vendor.mkdir(parents=True, exist_ok=True)
    before_dir = dir_extracted_folder / pyproject.package_name
    after_dir = dir_lambda_app_vendor / pyproject.package_name
    shutil.move(f"{before_dir}", f"{after_dir}")

    logger.info("done", indent=1)

    # download existing deployed json file, if possible
    download_deployed_json(env_name)

    # run chalice deploy command
    logger.info("run 'chalice deploy ...' command")
    args = [
        f"{bin_chalice}",
        "--project-dir",
        f"{dir_lambda_app}",
        "deploy",
        "--stage",
        env_name,
    ]
    logger.info("run cmd: {}".format(" ".join(args)), indent=1)
    with bsm.awscli():
        res = subprocess.run(args, capture_output=True)
    if res.returncode == 0:
        pass
    else:
        logger.info(f"return code: {res.returncode}", indent=1)
        logger.error(f"{Emoji.error} chalice deploy failed!")
        logger.error(res.stderr.decode("utf-8"))
        raise SystemError

    func_prefix = f"{config.env.chalice_app_name}-{env_name}"
    lambda_func_prefix_console_url = (
        f"https://{bsm.aws_region}.console.aws.amazon.com/"
        f"lambda/home?region={bsm.aws_region}#/"
        f"functions?fo=and&k0=functionName&o0=%3A&v0={func_prefix}"
    )
    logger.info(f"preview all deployed function at {lambda_func_prefix_console_url}")

    # update the deployed JSON file
    s3path_deployed_json = upload_deployed_json(
        env_name,
        lambda_function_hash=lambda_function_hash,
    )

    # in CI, post the deployed Lambda Function console url to the PR comment if possible
    if IS_CI:
        comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
        if comment_id:
            content = "\n".join(
                [
                    f"{Emoji.succeeded} {Emoji.awslambda} **Deploy Lambda app succeeded**",
                    f"",
                    f"- **source code version**: {__version__}",
                    f"- review [Lambda Functions]({lambda_func_prefix_console_url})",
                    f"- review [Lambda Source Artifacts]({s3dir_lambda_source.console_url})",
                    f"- review deployed [{config.env.env_name}.json file]({s3path_deployed_json.console_url})",
                ]
            )
            better_boto.post_comment_reply(
                bsm=bsm,
                in_reply_to=comment_id,
                content=content,
            )


@logger.block(
    msg="Deploy Lambda App with Chalice",
    start_emoji=f"{Emoji.deploy} {Emoji.awslambda}",
    end_emoji=Emoji.deploy,
    pipe=Emoji.awslambda,
)
def deploy_lambda_app(
    env_name: str = CURRENT_ENV,
    check: bool = True,
):
    try:
        if check:
            if (
                _do_we_deploy_lambda(
                    env_name=env_name,
                    is_ci_runtime=IS_CI,
                    branch_name=GIT_BRANCH_NAME,
                    is_lambda_branch=IS_LAMBDA_BRANCH,
                    is_int_branch=IS_INT_BRANCH,
                    is_release_branch=IS_RELEASE_BRANCH,
                )
                is False
            ):
                return
        run_update_chalice_config_script()
        lambda_function_hash = get_lambda_function_hash()
        if check:
            if do_we_deploy_lambda_based_on_hash(lambda_function_hash) is False:
                return
        with logger.nested():
            build_lambda_source_artifacts()
            run_chalice_deploy(env_name, lambda_function_hash)
        logger.info(f"{Emoji.succeeded} Deploy Lambda app succeeded!")
    except Exception as e:
        logger.error(f"{Emoji.failed} Deploy Lambda app failed!")
        # in CI, post the error message to the PR comment if possible
        if IS_CI:
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                content = "\n".join(
                    [
                        f"{Emoji.failed} Deploy Lambda app failed!",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
        raise e


@logger.block(
    msg="Run Chalice Delete",
    start_emoji=f"{Emoji.delete} {Emoji.awslambda}",
    end_emoji=Emoji.delete,
    pipe=Emoji.awslambda,
)
def run_chalice_delete(env_name: str):
    """
    Delete lambda app using chalice.

    :return: a boolean flag to indicate that if delete is successful.
    """
    # download existing deployed json file, if possible
    flag = download_deployed_json(env_name)
    if flag is False:
        logger.info("the deployed json file is not found, skip 'chalice delete ...'")
        return False

    # run chalice delete command
    logger.info("run 'chalice delete ...' command")
    args = [
        f"{bin_chalice}",
        "--project-dir",
        f"{dir_lambda_app}",
        "delete",
        "--stage",
        env_name,
    ]
    logger.info("run cmd: {}".format(" ".join(args)), indent=1)
    with bsm.awscli():
        res = subprocess.run(args)
    if res.returncode == 0:
        pass
    else:
        logger.info(f"return code: {res.returncode}", indent=1)
        logger.error(f"{Emoji.error} chalice delete failed!")
        raise SystemError

    func_prefix = f"{config.env.chalice_app_name}-{env_name}"
    lambda_func_prefix_console_url = (
        f"https://{bsm.aws_region}.console.aws.amazon.com/"
        f"lambda/home?region={bsm.aws_region}#/"
        f"functions?fo=and&k0=functionName&o0=%3A&v0={func_prefix}"
    )
    logger.info(f"verify all deleted function at {lambda_func_prefix_console_url}")

    # update the deployed JSON file
    s3path_deployed_json = upload_deployed_json(
        env_name, lambda_function_hash="deleted"
    )

    if IS_CI:
        comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
        if comment_id:
            content = "\n".join(
                [
                    f"{Emoji.succeeded} {Emoji.awslambda} **Delete Lambda app succeeded**",
                    f"",
                    f"- review [Lambda Functions]({lambda_func_prefix_console_url})",
                    f"- review deployed [{config.env.env_name}.json file]({s3path_deployed_json.console_url})",
                ]
            )
            better_boto.post_comment_reply(
                bsm=bsm,
                in_reply_to=comment_id,
                content=content,
            )
    return True


@logger.block(
    msg="Delete Lambda App with Chalice",
    start_emoji=f"{Emoji.delete} {Emoji.awslambda}",
    end_emoji=Emoji.delete,
    pipe=Emoji.awslambda,
)
def delete_lambda_app(
    env_name: str = CURRENT_ENV,
    check: bool = True,
):
    try:
        if check:
            if (
                do_we_delete_lambda(
                    env_name=env_name,
                    is_ci_runtime=IS_CI,
                    is_clean_up_branch=IS_CLEAN_UP_BRANCH,
                    commit_message_has_lbd=COMMIT_MESSAGE_HAS_LBD,
                )
                is False
            ):
                return
        run_update_chalice_config_script()
        with logger.nested():
            run_chalice_delete(env_name)
        logger.info(f"{Emoji.succeeded} Delete Lambda app succeeded!")
    except Exception as e:
        logger.error(f"{Emoji.failed} Delete Lambda app failed!")
        if IS_CI:
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                content = "\n".join(
                    [
                        f"{Emoji.failed} Delete Lambda app failed!",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
        raise e
