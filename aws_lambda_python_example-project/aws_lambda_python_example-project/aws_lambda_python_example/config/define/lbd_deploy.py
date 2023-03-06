# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from datetime import datetime

from s3pathlib import S3Path

if T.TYPE_CHECKING:
    from .main import Env


@dataclasses.dataclass
class LambdaDeployMixin:
    @property
    def chalice_app_name(self: "Env") -> str:
        return self.project_name_snake

    @property
    def lambda_layer_name(self: "Env") -> str:
        return self.project_name_snake

    # --------------------------------------------------------------------------
    # Temp folder
    #
    # Below are the folders that temporarily store the deployment artifacts
    # and the deployment script will deploy from temp location
    # if deployment succeeded, the artifacts will be moved to a target location
    # as an immutable record
    # --------------------------------------------------------------------------
    @property
    def s3dir_tmp_lambda_source(self: "Env") -> S3Path:
        """
        example: ``${s3dir_artifacts}/tmp/source.zip``
        """
        return self.s3dir_tmp.joinpath("source.zip")

    @property
    def s3dir_tmp_lambda_layer_zip(self: "Env") -> S3Path:
        """
        example: ``${s3dir_artifacts}/tmp/layer.zip``
        """
        return self.s3dir_tmp.joinpath("layer.zip")

    @property
    def s3dir_tmp_lambda_layer_requirements_txt(self: "Env") -> S3Path:
        """
        example: ``${s3dir_artifacts}/tmp/requirements.txt``
        """
        return self.s3dir_tmp.joinpath("requirements.txt")

    # --------------------------------------------------------------------------
    # Lambda related S3 location
    #
    # Enumerate important S3 location for Lambda Function artifacts.
    # --------------------------------------------------------------------------
    @property
    def s3dir_lambda(self: "Env") -> S3Path:
        """
        example: ``${s3dir_artifacts}/lambda/``
        """
        return self.s3dir_artifacts.joinpath("lambda").to_dir()

    @property
    def s3dir_lambda_source(self: "Env") -> S3Path:
        """
        example: ``${s3dir_artifacts}/lambda/source/``
        """
        return self.s3dir_lambda.joinpath("source").to_dir()

    @property
    def s3dir_lambda_layer(self: "Env") -> S3Path:
        """
        example: ``${s3dir_artifacts}/lambda/layer/``
        """
        return self.s3dir_lambda.joinpath("layer").to_dir()

    def get_s3path_lambda_layer_zip(
        self: "Env",
        version: int,
    ) -> S3Path:
        """
        example: ``${s3dir_artifacts}/lambda/source/${layer_version}/layer.zip``
        """
        return self.s3dir_lambda_layer.joinpath(
            str(version).zfill(6),
            "layer.zip",
        )

    def get_s3path_lambda_layer_requirements_txt(
        self: "Env",
        version: int,
    ) -> S3Path:
        """
        example: ``${s3dir_artifacts}/lambda/source/${layer_version}/requirements.txt``
        """
        return self.s3dir_lambda_layer.joinpath(
            str(version).zfill(6),
            "requirements.txt",
        )

    def get_s3dir_lambda_source(
        self: "Env",
        version: str,
    ) -> S3Path:
        """
        example: ``${s3dir_artifacts}/lambda/source/${source_version}/``
        """
        return self.s3dir_lambda_source.joinpath(f"{version}").to_dir()

    @property
    def s3dir_deployed(self: "Env") -> S3Path:
        """
        `AWS Chalice <https://aws.github.io/chalice/>`_ use ``deployed.json``
        to store the deployed resources. It is better to store all of
        historical ``deployed.json`` files somewhere as a record.

        example: ``${s3dir_artifacts}/lambda/deployed/``
        """
        return self.s3dir_lambda.joinpath("deployed").to_dir()

    def get_s3path_deployed_json(self: "Env", stage: str) -> S3Path:
        """
        example: ``${s3dir_artifacts}/lambda/deployed/dev.json``
        """
        return self.s3dir_deployed.joinpath(f"{stage}.json")

    def get_s3path_deployed_json_backup(self: "Env", stage: str) -> S3Path:
        """
        example: ``${s3dir_artifacts}/lambda/deployed/dev-${datetime}.json``
        """
        time_str = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S.%f")
        return self.s3dir_deployed.joinpath(f"{stage}-{time_str}.json")
