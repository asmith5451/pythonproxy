import sys
import os
import grp
import signal
import daemon
import lockfile

from .server import (
    serve,
    teardown,
    reload_config
)

def main(args = None):
    cwd_path = os.path.dirname(__file__)
    pid_path = os.path.join(cwd_path, 'run/echidna.pid')

    print(cwd_path, file=sys.stderr)
    print(pid_path, file=sys.stderr)

    context = daemon.DaemonContext(
        working_directory = cwd_path,
        pidfile=lockfile.FileLock(pid_path)
    )

    context.signal_map = {
        signal.SIGTERM: teardown,
        signal.SIGHUP: 'terminate',
        signal.SIGUSR1: reload_config
    }

    # The main routine.
    if args is None:
        args = sys.argv[1:]

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.

    with context:
        serve()


if __name__ == "__main__":
    main()
