# -*- coding: utf-8 -*-

"""
Parse the ``pyproject.toml`` file.
"""

import dataclasses
from pathlib import Path

import tomli

dir_project_root = Path(__file__).absolute().parent.parent.parent
path_pyproject_toml = dir_project_root / "pyproject.toml"


@dataclasses.dataclass
class PyProject:
    package_name: str = dataclasses.field()
    package_version: str = dataclasses.field()
    python_version: str = dataclasses.field()

    @classmethod
    def new(cls):
        toml_dict = tomli.loads(path_pyproject_toml.read_text())
        package_name = toml_dict["tool"]["poetry"]["name"]
        package_version = toml_dict["tool"]["poetry"]["version"]

        # good example: ^3.8.X
        _python_version = toml_dict["tool"]["poetry"]["dependencies"]["python"]
        _python_version_info = [
            token.strip()
            for token in (
                "".join(
                    [char if char.isdigit() else " " for char in _python_version]
                ).split()
            )
            if token.strip()
        ]
        python_version = f"{_python_version_info[0]}.{_python_version_info[1]}"
        return cls(
            package_name=package_name,
            package_version=package_version,
            python_version=python_version,
        )


pyproject = PyProject.new()
