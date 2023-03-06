# -*- coding: utf-8 -*-

from rich.console import Console

from .nested_logger import NestedLogger
from .emoji import Emoji


class Logger(NestedLogger):
    def block(
        self,
        msg: str,
        start_emoji: str = "",
        end_emoji: str = "",
        pipe: str = "| ",
    ):
        return self.pretty_log(
            start_msg=f"{Emoji.start_timer} {start_emoji} {msg}",
            end_msg=f"{Emoji.end_timer} {end_emoji} End '{msg}', elapsed = {{elapsed:.2f}} sec",
            pipe=pipe,
        )


logger = Logger(
    name="automation",
    log_format="%(message)s",
)

console = Console()
