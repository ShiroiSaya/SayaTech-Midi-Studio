from __future__ import annotations

import json
import os
import platform
import sys
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .app_paths import logs_dir

_SESSION_ID = datetime.now().strftime('%Y%m%d_%H%M%S') + f'_pid{os.getpid()}'
_RUNTIME_LOG_PATH: Optional[Path] = None
_CRASH_DIR: Optional[Path] = None
_ORIGINAL_SYS_EXCEPTHOOK = sys.excepthook
_ORIGINAL_THREADING_EXCEPTHOOK = getattr(threading, 'excepthook', None)
_RUNTIME_DEBUG_ENABLED = False


def log_dir() -> Path:
    global _CRASH_DIR
    if _CRASH_DIR is None:
        _CRASH_DIR = logs_dir()
        _CRASH_DIR.mkdir(parents=True, exist_ok=True)
    return _CRASH_DIR


def runtime_log_path() -> Path:
    global _RUNTIME_LOG_PATH
    if _RUNTIME_LOG_PATH is None:
        _RUNTIME_LOG_PATH = log_dir() / f'runtime_{_SESSION_ID}.log'
    return _RUNTIME_LOG_PATH


def _now() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def set_runtime_debug_mode(enabled: bool) -> None:
    global _RUNTIME_DEBUG_ENABLED
    _RUNTIME_DEBUG_ENABLED = bool(enabled)


def append_runtime_log(message: str, *, debug: bool = False) -> None:
    if debug and not _RUNTIME_DEBUG_ENABLED:
        return
    try:
        with runtime_log_path().open('a', encoding='utf-8') as f:
            f.write(f'[{_now()}] {message}\n')
    except Exception:
        pass


def _safe_jsonable(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return {str(k): _safe_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_safe_jsonable(v) for v in value]
    return repr(value)


def write_crash_log(title: str, exc: BaseException, context: Optional[Dict[str, Any]] = None) -> str:
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
    path = log_dir() / f'crash_{stamp}_pid{os.getpid()}.log'
    payload = {
        'title': title,
        'timestamp': _now(),
        'python': sys.version,
        'platform': platform.platform(),
        'executable': sys.executable,
        'argv': sys.argv,
        'cwd': os.getcwd(),
        'thread': threading.current_thread().name,
        'exception_type': type(exc).__name__,
        'exception_message': str(exc),
        'traceback': ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
        'context': _safe_jsonable(context or {}),
        'runtime_log_path': str(runtime_log_path()),
        'session_id': _SESSION_ID,
    }
    with path.open('w', encoding='utf-8') as f:
        f.write(json.dumps(payload, ensure_ascii=False, indent=2))
        f.write('\n')
    append_runtime_log(f'已生成崩溃日志：{path.name} | {type(exc).__name__}: {exc}', debug=True)
    return str(path)


def install_global_hooks() -> None:
    append_runtime_log('Crash logging initialized.', debug=True)

    def sys_hook(exc_type, exc_value, exc_tb):
        if exc_type is KeyboardInterrupt:
            if _ORIGINAL_SYS_EXCEPTHOOK:
                _ORIGINAL_SYS_EXCEPTHOOK(exc_type, exc_value, exc_tb)
            return
        try:
            write_crash_log(
                'Unhandled exception in main thread',
                exc_value,
                {
                    'hook': 'sys.excepthook',
                    'traceback_text': ''.join(traceback.format_exception(exc_type, exc_value, exc_tb)),
                },
            )
        finally:
            if _ORIGINAL_SYS_EXCEPTHOOK:
                _ORIGINAL_SYS_EXCEPTHOOK(exc_type, exc_value, exc_tb)

    sys.excepthook = sys_hook

    if _ORIGINAL_THREADING_EXCEPTHOOK is not None:
        def thread_hook(args):
            try:
                if args.exc_type is not KeyboardInterrupt and args.exc_value is not None:
                    write_crash_log(
                        f'Unhandled exception in thread {args.thread.name}',
                        args.exc_value,
                        {
                            'hook': 'threading.excepthook',
                            'thread_name': args.thread.name,
                            'thread_ident': args.thread.ident,
                            'traceback_text': ''.join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)),
                        },
                    )
            finally:
                _ORIGINAL_THREADING_EXCEPTHOOK(args)

        threading.excepthook = thread_hook
