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
import daemon
import logging

from .pidfile import pidfile
from .server import (servers, serve)

def main(args=None):
    working_directory = os.path.dirname(__file__)
    
    # get arguments from command line if not passed directly
    if args is None:
        args = sys.argv[1:]
    
    logger = logging.getLogger("echidna")
    
    fm = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(filename = os.path.join(working_directory, "echidna.log"))
    fh.setFormatter(fm)
    fh.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    
    logger.addHandler(fh)

    # create daemon context
    context = daemon.DaemonContext(
        working_directory = working_directory,
        pidfile = pidfile('/tmp/echidna.pid'),
        files_preserve = [fh.stream]
    )
    
    logger.debug("starting daemon")
    
    # create server and begin listenning
    try: 
        with context, servers() as s:
            logger.debug("serving servers!")
            serve(s)
    except Exception as err:
        logger.debug("error: %s", err)
    
    logger.debug("finishing daemon")

if __name__ == "__main__":
    main()
