import sys
import os
import grp
import signal
import daemon

from .server import (
    serve,
    teardown,
    reload_config
)

def main(args = None):
    cwd_path = os.path.dirname(__file__)

    # TODO: research PID file locking since lockfile is depricated and doesn't
    # seem to work

    context = daemon.DaemonContext(
        working_directory = cwd_path,
    )

    context.signal_map = {
        signal.SIGTERM: teardown,
        signal.SIGHUP: 'terminate',
        signal.SIGUSR1: reload_config
    }

    # get arguments from command line if not passed directly
    if args is None:
        args = sys.argv[1:]

    # TODO: handle arguments for start, stop, restart, and reload

    with context:
        serve()

if __name__ == "__main__":
    main()
