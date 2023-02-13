# -*- coding: utf-8 -*-

import typing as T
import sys
import time
import itertools


class Waiter:
    """
    Simple retry / poll with progress.
    """
    def __init__(
        self,
        delays: T.Union[int, float],
        timeout: T.Union[int, float],
        indent: int = 0,
        verbose: bool = True,
    ):
        self.delays = itertools.repeat(delays)
        self.timeout = timeout
        self.tab = " " * indent
        self.verbose = verbose

    def __iter__(self):
        start = time.time()
        end = start + self.timeout
        for attempt, delay in enumerate(self.delays, 1):
            now = time.time()
            remaining = end - now
            if remaining < 0:
                raise TimeoutError(f"timed out in {self.timeout} seconds!")
            else:
                time.sleep(min(delay, remaining))
                elapsed = int(now - start + delay)
                if self.verbose:
                    sys.stdout.write(
                        f"\r{self.tab}on {attempt} th attempt, "
                        f"elapsed {elapsed} seconds, "
                        f"remain {self.timeout - elapsed} seconds ..."
                    )
                    sys.stdout.flush()
                yield attempt, int(elapsed)
