from __future__ import annotations

import os
import sys
from typing import Sequence


def is_windows() -> bool:
    return os.name == "nt"


def is_admin() -> bool:
    if not is_windows():
        return False
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin(argv: Sequence[str]) -> bool:
    if not is_windows():
        return False
    try:
        import ctypes
        shell32 = ctypes.windll.shell32
        if getattr(sys, "frozen", False):
            executable = sys.executable
            params = " ".join(_quote_arg(arg) for arg in argv[1:])
        else:
            executable = sys.executable
            script_path = os.path.abspath(argv[0])
            params = " ".join([_quote_arg(script_path), *(_quote_arg(arg) for arg in argv[1:])])
        rc = shell32.ShellExecuteW(None, "runas", executable, params, None, 1)
        return rc > 32
    except Exception:
        return False


def _quote_arg(arg: str) -> str:
    return '"' + str(arg).replace('"', '\"') + '"'
