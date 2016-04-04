import os
import sys
import signal
import daemon
from lockfile.pidlockfile import PIDLockFile

from .server import (
    serve,
    teardown,
    reload_config
)


def main(args=None):
    # get arguments from command line if not passed directly
    if args is None:
        args = sys.argv[1:]

    context = daemon.DaemonContext(
        working_directory = os.path.dirname(__file__),
        pidfile = PIDLockFile('/tmp/echidna.pid')
    )

    context.signal_map = {
        signal.SIGTERM: teardown,
        signal.SIGHUP: 'terminate',
        signal.SIGUSR1: reload_config
    }

    with context:
        serve()

if __name__ == "__main__":
    main()
