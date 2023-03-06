# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from s3pathlib import S3Path

if T.TYPE_CHECKING:
    from .main import Env


@dataclasses.dataclass
class AppMixin:
    username: T.Optional[str] = dataclasses.field(default=None)
    password: T.Optional[str] = dataclasses.field(default=None)

    s3uri_source: T.Optional[str] = dataclasses.field(default=None)
    s3uri_target: T.Optional[str] = dataclasses.field(default=None)

    @property
    def s3dir_source(self) -> S3Path:
        return S3Path.from_s3_uri(self.s3uri_source).to_dir()

    @property
    def s3dir_target(self) -> S3Path:
        return S3Path.from_s3_uri(self.s3uri_target).to_dir()
