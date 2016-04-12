"""
Copyright (c) 2016 Kickback Rewards Systems

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os
import sys
import signal
import daemon
import logging

from .pidfile import pidfile
from .server import (build_servers, serve_servers, close_servers)

def main(args=None):
    working_directory = os.path.dirname(__file__)
    
    # get arguments from command line if not passed directly
    if args is None:
        args = sys.argv[1:]
    
    # setup logging
    handler = setup_handler(os.path.join(working_directory, "echidna.log"))
    logger = setup_logger("echidna", handler, logging.DEBUG)
    
    logger.info("starting daemon")
   
    try:
        # this logic should be encapuslated into the new daemon runner class
        
        # servers have to be created inside the daemon context, but need to be
        # accessible outside of it for the teardown function.
        servers = None
        
        # scoped teardown
        def teardown(signum, frame):
            close_servers(servers)
        
        # create daemon context
        context = daemon.DaemonContext(
            working_directory = working_directory,
            pidfile = pidfile('/tmp/echidna.pid'),
            files_preserve = [handler.stream],
            signal_map = {
                signal.SIGTERM: teardown,
                signal.SIGHUP: 'terminate'
            }
        )
        
        # create servers and begin listenning
        with context:
            servers = build_servers()
            serve_servers(servers)
    
    except Exception as err:
        logger.info("unhandled error: %s", err)
    
    logger.info("daemon stopped")

def setup_handler(file):
    fm = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(filename = file)
    fh.setFormatter(fm)
    return fh
    
def setup_logger(name, handler, level):
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger

if __name__ == "__main__":
    main()
