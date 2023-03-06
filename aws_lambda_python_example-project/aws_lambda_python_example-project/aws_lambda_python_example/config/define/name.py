# -*- coding: utf-8 -*-

import dataclasses


@dataclasses.dataclass
class NameMixin:
    """
    This mixin class derive all AWS Resource name based on the project name
    and the env name.
    """
