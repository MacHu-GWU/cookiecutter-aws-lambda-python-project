# -*- coding: utf-8 -*-

import typing as T
from pathlib_mate import Path


def count_line_in_file(path: Path) -> int:
    return path.read_text().count("\n") + 1


def count_line_in_dir(path: Path) -> int:
    return sum([count_line_in_file(p) for p in path.select_by_ext(".py")])


def count_line_in_many_dir(dir_list: T.List[Path]) -> int:
    return sum([count_line_in_dir(p) for p in dir_list])


dir_here = Path.dir_here(__file__)

app_code = count_line_in_many_dir(
    [
        dir_here / "{{ cookiecutter.package_name }}",
        dir_here / "lambda_app",
    ]
)
test_code = count_line_in_many_dir(
    [
        dir_here / "tests",
        dir_here / "tests_int",
    ]
)
ops_code = count_line_in_many_dir(
    [
        dir_here / "bin",
    ]
)

print(f"app_code: {app_code}")
print(f"test_code: {test_code}")
print(f"ops_code: {ops_code}")
