# -*- coding: utf-8 -*-

"""
Enhance the default logger, print visual ascii effect for better readability.

Usage::

    from logger import logger

.. note::

    This module is "ZERO-DEPENDENCY".
"""

import typing as T
import sys
import enum
import logging
import contextlib
from functools import wraps
from datetime import datetime


def create_logger(
    name: T.Optional[str] = None,
    level: int = logging.INFO,
    log_format: str = "[User %(asctime)s] %(message)s",
    datetime_format: str = "%Y-%m-%d %H:%m:%S",
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(level)
    formatter = logging.Formatter(
        fmt=log_format,
        datefmt=datetime_format,
    )
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


tab = " " * 2


def encode_pipe(pipe: str) -> str:
    if len(pipe) == 1:
        return pipe + " "
    elif len(pipe) == 2:
        if pipe[1] == " ":
            return pipe
        else:
            raise ValueError
    else:
        raise ValueError


DEFAULT_PIPE = encode_pipe("| ")


def format_line(
    msg: str,
    indent: int = 0,
    nest: int = 0,
    _pipes: T.Optional[T.List[str]] = None,
) -> str:
    """
    Format message with indentation and nesting.

    Example::

        >>> format_line("hello")
        '[User] | hello'
        >>> format_line("hello", indent=1)
        '[User] |   hello'
        >>> format_line("hello", nest=1)
        '[User] | | hello'
        >>> format_line("hello", indent=1, nest=1)
        '[User] | |   hello'
    """
    if _pipes is None:
        _pipes = [
            DEFAULT_PIPE,
        ] * (nest + 1)
    else:
        if len(_pipes) != (nest + 1):
            raise ValueError
    nesting = "".join(_pipes)
    return f"{nesting}{tab * indent}{msg}"


class AlignEnum(str, enum.Enum):
    left = "<"
    right = ">"
    middle = "^"


def format_ruler(
    msg: str,
    char: str = "-",
    align: AlignEnum = AlignEnum.middle,
    length: int = 80,
    left_padding: int = 5,
    right_padding: int = 5,
    corner: str = "",
    nest: int = 0,
    _pipes: T.Optional[T.List[str]] = None,
) -> str:
    """
    Format message to shape a horizontal ruler.

    :param msg: the message to print
    :param char: the character to use as ruler
    :param align: left, middle, right alignment of the message
    :param length: the total number of character of the ruler
    :param left_padding: the number of ruler character to pad on the left
    :param right_padding: the number of ruler character to pad on the right
    :param corner: the character to use as corner
    :param nest: the number of pipe to print before the ruler

    Example::

        >>> format_ruler("Hello", length=40)
        '---------------- Hello -----------------'

        >>> format_ruler("Hello", length=20)
        '------ Hello -------'

        >>> format_ruler("Hello", char="=", length=40)
        '================ Hello ================='

        >>> format_ruler("Hello", corner="+", length=40)
        '+--------------- Hello ----------------+'

        >>> format_ruler("Hello", align=AlignEnum.left, length=40)
        '----- Hello ----------------------------'

        >>> format_ruler("Hello", align=AlignEnum.right, length=40)
        '---------------------------- Hello -----'

        >>> format_ruler("Hello", left_padding=3, align=AlignEnum.left, length=40)
        '--- Hello ------------------------------'

        >>> format_ruler("Hello", right_padding=3, align=AlignEnum.right, length=40)
        '------------------------------ Hello ---'
    """
    length = length - len(corner) * 2 - left_padding - right_padding - nest * 2
    msg = f" {msg} "
    left_pad = char * left_padding
    right_pad = char * right_padding
    if _pipes is None:
        _pipes = [
            DEFAULT_PIPE,
        ] * nest
    else:
        if len(_pipes) != nest:
            raise ValueError
    nesting = "".join(_pipes)
    s = f"{nesting}{corner}{left_pad}{msg:{char}{align}{length{% raw %}}}{% endraw %}{right_pad}{corner}"
    return s


def decohints(decorator: T.Callable) -> T.Callable:
    """
    fix pycharm type hint bug for decorator.
    """
    return decorator


class NestedLogger:
    def __init__(
        self,
        logger: T.Optional[logging.Logger] = None,
        name: T.Optional[str] = None,
        level: int = logging.INFO,
        log_format: str = "[User %(asctime)s] %(message)s",
        datetime_format: str = "%Y-%m-%d %H:%m:%S",
    ):
        if logger is None:
            self._logger = create_logger(
                name=name,
                level=level,
                log_format=log_format,
                datetime_format=datetime_format,
            )
        else:
            self._logger = logger

        self._nest = 0
        self._pipes = [
            DEFAULT_PIPE,
        ]

    def _pipe_start(
        self,
        pipe: T.Optional[str] = None,
    ) -> T.Optional[str]:
        if pipe is not None:
            pipe = encode_pipe(pipe)
            current_pipe = self._pipes.pop()
            self._pipes.append(pipe)
            return current_pipe
        else:
            return None

    def _pipe_end(
        self, pipe: T.Optional[str] = None, last_Pipe: T.Optional[str] = None
    ):
        if pipe is not None:
            self._pipes.pop()
            self._pipes.append(last_Pipe)

    @contextlib.contextmanager
    def pipe(
        self,
        pipe: T.Optional[str] = None,
    ):
        last_pipe = self._pipe_start(pipe)
        try:
            yield self
        finally:
            self._pipe_end(pipe, last_pipe)

    def _log(
        self,
        func: T.Callable,
        msg: str,
        indent: int = 0,
        pipe: T.Optional[str] = None,
    ) -> str:
        with self.pipe(pipe=pipe):
            lines = msg.split("\n")
            for line in lines:
                output = format_line(line, indent, self._nest, self._pipes)
                func(output)
        return output

    def debug(
        self,
        msg: str,
        indent: int = 0,
        pipe: T.Optional[str] = None,
    ) -> str:  # pragma: no cover
        return self._log(self._logger.debug, msg, indent, pipe)

    def info(
        self,
        msg: str,
        indent: int = 0,
        pipe: T.Optional[str] = None,
    ) -> str:
        return self._log(self._logger.info, msg, indent, pipe)

    def warning(
        self,
        msg: str,
        indent: int = 0,
        pipe: T.Optional[str] = None,
    ) -> str:  # pragma: no cover
        return self._log(self._logger.warning, msg, indent, pipe)

    def error(
        self,
        msg: str,
        indent: int = 0,
        pipe: T.Optional[str] = None,
    ) -> str:  # pragma: no cover
        return self._log(self._logger.error, msg, indent, pipe)

    def critical(
        self,
        msg: str,
        indent: int = 0,
        pipe: T.Optional[str] = None,
    ) -> str:  # pragma: no cover
        return self._log(self._logger.critical, msg, indent, pipe)

    def ruler(
        self,
        msg: str,
        char: str = "-",
        align: AlignEnum = AlignEnum.left,
        length: int = 80,
        left_padding: int = 5,
        right_padding: int = 5,
        corner: str = "+",
        pipe: T.Optional[str] = None,
        func: T.Optional[T.Callable] = None,
    ) -> str:
        if func is None:
            func = self._logger.info

        with self.pipe(pipe=pipe):
            output = format_ruler(
                msg,
                char,
                align,
                length,
                left_padding,
                right_padding,
                corner,
                self._nest,
                self._pipes[:-1],
            )
            func(output)
        return output

    def _nested_start(
        self,
        pipe: T.Optional[str] = None,
    ):
        self._nest += 1

        if pipe is None:
            self._pipes.append(DEFAULT_PIPE)
        else:
            self._pipes.append(encode_pipe(pipe))

    def _nested_end(self):
        self._nest -= 1
        self._pipes.pop()

    @contextlib.contextmanager
    def nested(
        self,
        pipe: T.Optional[str] = None,
    ):
        self._nested_start(pipe=pipe)
        try:
            yield self
        finally:
            self._nested_end()

    def pretty_log(
        self,
        start_msg: str = "Start {func_name}()",
        error_msg: str = "Error, elapsed = {elapsed:.2f} sec",
        end_msg: str = "End {func_name}(), elapsed = {elapsed:.2f} sec",
        char: str = "-",
        align: AlignEnum = AlignEnum.left,
        length: int = 80,
        left_padding: int = 5,
        right_padding: int = 5,
        corner: str = "+",
        nest: int = 0,
        pipe: T.Optional[str] = None,
    ):
        """
        Pretty print ruler when a function start, error, end.

        ``start_msg``, ``error_msg`` and ``end_msg`` are string template.
        the ``{func_name}`` will become the function you are decorating,
        the ``{elapsed}`` will become the execution time of the function.
        You can use ``{elapsed:.2f}`` to set the precision to two digits.
        The execution time measurement are not accuracy, it is just an estimation
        up to three digits precision.

        Example:

        .. code-block:: python

            @nested_logger.pretty_log(nest=1)
            def my_func2(name: str):
                time.sleep(1)
                nested_logger.info(f"{name} do something in my func 2")

            @nested_logger.pretty_log()
            def my_func1(name: str):
                time.sleep(1)
                nested_logger.info(f"{name} do something in my func 1")
                my_func2(name="bob")

            my_func1(name="alice")

        The output looks like::

            [User] +----- Start my_func1() ------------------------------------+
            [User] |
            [User] | alice do something in my func 1
            [User] | +----- Start my_func2() ----------------------------------+
            [User] | |
            [User] | | bob do something in my func 2
            [User] | |
            [User] | +----- End my_func2(), elapsed = 1 sec -------------------+
            [User] |
            [User] +----- End my_func1(), elapsed = 2 sec ---------------------+
        """

        @decohints
        def deco(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                st = datetime.utcnow()

                for _ in range(nest):
                    self._nested_start(pipe=pipe)

                if nest == 0 and (pipe is not None):
                    last_pipe = self._pipe_start(pipe)

                self.ruler(
                    msg=start_msg.format(func_name=func.__name__),
                    char=char,
                    align=align,
                    length=length,
                    left_padding=left_padding,
                    right_padding=right_padding,
                    corner=corner,
                )
                self.info("")

                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    et = datetime.utcnow()
                    elapsed = (et - st).total_seconds()
                    self.info("")
                    self.ruler(
                        msg=error_msg.format(elapsed=elapsed),
                        char=char,
                        align=align,
                        length=length,
                        left_padding=left_padding,
                        right_padding=right_padding,
                        corner=corner,
                    )
                    raise e

                et = datetime.utcnow()
                elapsed = (et - st).total_seconds()
                self.info("")
                self.ruler(
                    msg=end_msg.format(func_name=func.__name__, elapsed=elapsed),
                    char=char,
                    align=align,
                    length=length,
                    left_padding=left_padding,
                    right_padding=right_padding,
                    corner=corner,
                )

                for _ in range(nest):
                    self._nested_end()

                if nest == 0 and (pipe is not None):
                    self._pipe_end(pipe, last_pipe)

                return result

            return wrapper

        return deco

    @contextlib.contextmanager
    def disabled(
        self,
        disable: bool = True,
    ):
        try:
            if disable:
                existing_handlers = list(self._logger.handlers)
                self._logger.handlers.clear()
            yield self
        finally:
            if disable:
                for handler in existing_handlers:
                    self._logger.handlers.append(handler)
