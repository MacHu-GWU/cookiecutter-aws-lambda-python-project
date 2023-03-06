# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from s3pathlib import S3Path

if T.TYPE_CHECKING:
    from .main import Env


@dataclasses.dataclass
class CloudFormationMixin:
    @property
    def s3dir_cloudformation_templates(self: "Env") -> S3Path:  # pragma: no cover
        """
        Shared AWS CloudFormation storage s3 dir for all environments.
        """
        return self.s3dir_artifacts.joinpath("cloudformation", "templates").to_dir()
