import threading
from datetime import datetime


_lock = threading.Lock()

_last_check = None
_last_success = None
_last_error = None


def set_check_success():
    global _last_check
    global _last_success
    global _last_error

    now = datetime.now()

    with _lock:
        _last_check = now
        _last_success = now
        _last_error = None


def set_check_error(error):
    global _last_check
    global _last_error

    now = datetime.now()

    with _lock:
        _last_check = now
        _last_error = str(error)


def get_status():
    with _lock:
        return {
            "last_check": _last_check,
            "last_success": _last_success,
            "last_error": _last_error,
        }