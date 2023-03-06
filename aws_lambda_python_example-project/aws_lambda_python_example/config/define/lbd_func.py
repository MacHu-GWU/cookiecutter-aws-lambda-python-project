# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from s3pathlib import S3Path

if T.TYPE_CHECKING:
    from .main import Env


@dataclasses.dataclass
class LambdaFunctionMixin:
    def _get_func_fullname(self: "Env", shortname: str) -> str:
        return f"{self.chalice_app_name}-{self.env_name}-{shortname}"

    @property
    def func_name_hello(self: "Env") -> str:
        return "hello"

    @property
    def func_fullname_hello(self: "Env") -> str:
        return self._get_func_fullname(self.func_name_hello)

    @property
    def func_name_s3sync(self: "Env") -> str:
        return "s3sync"

    @property
    def func_fullname_s3sync(self: "Env") -> str:
        return self._get_func_fullname(self.func_name_s3sync)
