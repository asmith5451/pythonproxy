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
# https://www.youtube.com/watch?v=3r8s6hrssh8
import os
import sys
import signal
import socket
import socketserver
import logging
import daemon

from .pidfile import pidfile
from .server import ProxyServer
from .request import ProxyRequestHandler
from .settings import Settings

class ProxyDaemon(object):
    def __init__(self, working_directory, pid_directory):
        # get access to settings
        self.settings = Settings(working_directory)
        
        # setup logging
        self.logHandler = setup_handler(working_directory)
        self.logger = setup_logger("echidna", self.logHandler, logging.DEBUG)
        
        # create context
        self.context = daemon.DaemonContext(
            working_directory = working_directory,
            pidfile = pidfile(os.path.join(pid_directory, 'echidna.pid')),
            files_preserve = [self.logHandler.stream],
            signal_map = {
                signal.SIGTERM: self.teardown,
                signal.SIGHUP: 'terminate'
            }
        )
    
    def __enter__(self):
        self.logger.debug("entering daemon context")
        self.context.__enter__()
        
        self.logger.debug("creating listeners")
        self.servers = self._make_servers()
        return self
    
    def __exit__(self, type, value, traceback):
        if type is not None:
            self.logger.error("UNHANDLED EXCEPTION", exc_info=(type, value, traceback))
        
        self.logger.debug("cleanup listeners")
        self._finalize_servers()
        
        self.logger.info("exiting daemon context")
        self.context.__exit__()
    
    def _make_servers(self):
        return [make_server_node(s) for s in self.settings.servers()]
    
    def _finalize_servers(self):
        self.logger.debug("cleanup: %s", self.servers[0].server_address)
        # TODO: uncomment this whe shutdown bug resolved
        #self.servers[0].server_close()
    
    def teardown(self, signum, frame):
        self.logger.debug("stopping: %s", self.servers[0].server_address)
        # TODO: research why shutdown() causes hang
        #self.servers[0].shutdown()
        self.servers[0].server_close()
    
    def run(self):
        # todo multi-thread the server startups
        self.logger.debug("starting: %s", self.servers[0].server_address)
        # TODO: research if it's safe to ignore the ValueError caused by
        # the call to server.server_close()
        self.servers[0].serve_forever() 
 
def make_server_node(conf):
    # TODO: make this pretty
    host = conf[0]
    port = conf[1]
    dhost = conf[2]
    dport = conf[3]
        
    src = (host, port)
    dst = (dhost, dport)
    
    return ProxyServer(src, dst, ProxyRequestHandler)

def setup_handler(working_directory):
    f = os.path.join(working_directory, "echidna.log")
    frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(filename = f)
    fh.setFormatter(frmt)
    return fh
    
def setup_logger(name, handler, level):
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
