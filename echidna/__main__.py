import sys
import os
import grp
import signal
import daemon
import lockfile

from echidna.server import (
    setup,
    serve,
    teardown,
    reload_config
)

def main(args = None):
    """ The main routine. """
    if args is None:
        args = sys.argv[1:]

    print('This is the main routine.')
    print('It should do something interesting.')

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.

if __name__ == "__main__":
    main()
