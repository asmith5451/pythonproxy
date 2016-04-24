import os
from ..errors import DaemonProcessDetachError

def daemon_fork():
    """ Fork the daemon, and then exit. In the forked process, we create a new
        session which has the property of having no controlling terminal. Then
        we fork the daemon, and exit the parent process, ensring we have no
        active session, and the process is then a real daemon.
        """
    fork_then_exit(error_message = "failed first fork")
    os.setsid()
    fork_then_exit(error_message = "failed second fork")

def fork_then_exit(error_message):
    """ Fork the current process, and continue processing in the fork, but exit
        the original calling process. Using os._exit(0) exits without causing
        cleanup handlers to be triggered.
        """
    try:
        if os.fork() > 0:
            os._exit(0)
    except OSError as exc:
        raise DaemonProcessDetachError(
            "{message}: [{exc.errno:d}] {exc.strerror}".format(
                message = error_message,
                exc = exc)) from exc
