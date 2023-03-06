# -*- coding: utf-8 -*-

import sys

if sys.platform in ["win32", "cygwin"]:
    OPEN_COMMAND = "start"
else:
    OPEN_COMMAND = "open"
