from __future__ import annotations

import os
import sys
import threading
from typing import Sequence

_LOW_LATENCY_LOCK = threading.Lock()
_LOW_LATENCY_REFS = 0
_ORIGINAL_PRIORITY_CLASS: int | None = None


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


def enter_low_latency_mode() -> bool:
    if not is_windows():
        return False
    global _LOW_LATENCY_REFS, _ORIGINAL_PRIORITY_CLASS
    try:
        import ctypes
        winmm = ctypes.windll.winmm
        kernel32 = ctypes.windll.kernel32
        ABOVE_NORMAL_PRIORITY_CLASS = 0x00008000
        with _LOW_LATENCY_LOCK:
            if _LOW_LATENCY_REFS == 0:
                try:
                    winmm.timeBeginPeriod(1)
                except Exception:
                    pass
                try:
                    proc = kernel32.GetCurrentProcess()
                    _ORIGINAL_PRIORITY_CLASS = int(kernel32.GetPriorityClass(proc) or 0)
                    kernel32.SetPriorityClass(proc, ABOVE_NORMAL_PRIORITY_CLASS)
                except Exception:
                    _ORIGINAL_PRIORITY_CLASS = None
            _LOW_LATENCY_REFS += 1
        return True
    except Exception:
        return False


def leave_low_latency_mode() -> bool:
    if not is_windows():
        return False
    global _LOW_LATENCY_REFS, _ORIGINAL_PRIORITY_CLASS
    try:
        import ctypes
        winmm = ctypes.windll.winmm
        kernel32 = ctypes.windll.kernel32
        NORMAL_PRIORITY_CLASS = 0x00000020
        with _LOW_LATENCY_LOCK:
            if _LOW_LATENCY_REFS <= 0:
                return False
            _LOW_LATENCY_REFS -= 1
            if _LOW_LATENCY_REFS == 0:
                try:
                    winmm.timeEndPeriod(1)
                except Exception:
                    pass
                try:
                    proc = kernel32.GetCurrentProcess()
                    kernel32.SetPriorityClass(proc, int(_ORIGINAL_PRIORITY_CLASS or NORMAL_PRIORITY_CLASS))
                except Exception:
                    pass
                _ORIGINAL_PRIORITY_CLASS = None
        return True
    except Exception:
        return False


def _quote_arg(arg: str) -> str:
    return '"' + str(arg).replace('"', '\\"') + '"'
