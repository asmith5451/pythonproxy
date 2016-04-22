import os
from ..errors import DaemonProcessDetachError

def fork_then_exit(error_message):
    try:
        if os.fork() > 0:
            os._exit(0)
    except OSError as exc:
        raise DaemonProcessDetachError(
            "{message}: [{exc.errno:d}] {exc.strerror}".format(
                message = error_message,
                exc = exc)) from exc
