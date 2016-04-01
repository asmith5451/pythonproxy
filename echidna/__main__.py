import os
import sys
import signal
import daemon
from shutil import copyfile
from .pidfile import PIDFile

from .server import (
    serve,
    teardown,
    reload_config
)

def main(args = None):
    # get arguments from command line if not passed directly
    if args is None:
        args = sys.argv[1:]

    # TODO: take data_dir as a parameter in the cli

    # create directory to store program data
    data_dir = os.path.join(os.path.expanduser('~'), '.echidna')
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
        os.mkdir(os.path.join(data_dir, 'conf'))

    # TODO: make server use the data_dir for it's config. This requires that
    # the configuration file is created in, in a first run scenario, and then
    # used from that directory.
    conf_skel_dir = os.path.join(os.path.dirname(__file__), 'conf')

    # copy skeleton configuration
    config_file = os.path.join(data_dir, 'conf', 'server.ini')
    if not os.path.exists(config_file):
        copyfile(os.path.join(conf_skel_dir, 'server.ini'), config_file)

    # pidfile path
    pidfile = os.path.join(data_dir, 'echidna.pid')

    context = daemon.DaemonContext(
        working_directory = data_dir,
        pidfile = PIDFile(pidfile)
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
