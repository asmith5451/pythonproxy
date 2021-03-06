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
import threading

from .pidfile import pidfile
from .server import ProxyServer
from .request import ProxyRequestHandler
from .settings import Settings

class ProxyDaemon(object):
    def __init__(self, working_directory, pid_directory):
        # get access to settings
        self.settings = Settings(file_path(working_directory, "adam2.sqlite"))
        
        # setup logging
        fh = setup_logfile_handler(file_path(working_directory, "echidna.log"))
        self.logger = setup_logger(
            name = 'echidna',
            handler = fh,
            level = logging.DEBUG)
        
        # create context
        self.context = daemon.DaemonContext(
            working_directory = working_directory,
            pidfile = pidfile(file_path(pid_directory, "echidna.pid")),
            files_preserve = [fh.stream],
            signal_map = {
                signal.SIGTERM: self.teardown,
                signal.SIGHUP: 'terminate'
            }
        )
    
    def __enter__(self):
        self.logger.debug("entering daemon context")
        self.context.__enter__()
        
        self.logger.debug("creating listeners")
        self.servers = [make_server(s, self.logger) for s in self.settings.servers()]
        
        return self
    
    def __exit__(self, type, value, traceback):
        if type is not None:
            self.logger.error("UNHANDLED EXCEPTION", exc_info=(type, value, traceback))
        
        self.__finalize_servers()
        
        self.logger.info("exiting daemon context")
        self.context.__exit__()
    
    def __finalize_servers(self):
        self.logger.debug("cleanup listeners")
        for server in self.servers:
            self.logger.debug("cleanup: %s -> %s", server.server_address, server.dest_address)
            server.server_close()
    
    def teardown(self, signum, frame):
        self.logger.debug("stopping listeners")
        for server in self.servers:
            self.logger.debug("stopping: %s -> %s", server.server_address, server.dest_address)
            server.shutdown()
    
    def run(self, args):
        self.logger.debug("starting listeners")
        threads = [make_server_thread(s, self.logger) for s in self.servers]
        
        # start threads
        for thread in threads:
            thread.start()
        
        # wait for threads to finish
        for thread in threads:
            thread.join()

def make_server(conf, logger):
    logger.debug("creating: %s -> %s", conf['source'], conf['destination'])
    return ProxyServer(conf['source'], conf['destination'], ProxyRequestHandler)

def make_server_thread(server, logger):
    return threading.Thread(target=server_thread, args=(server,logger))

def server_thread(server, logger):
    logger.debug("starting: %s -> %s", server.server_address, server.dest_address)
    server.serve_forever()

def setup_logfile_handler(file):
    f = file
    frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(filename = f)
    fh.setFormatter(frmt)
    return fh
    
def setup_logger(name, handler, level):
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger

def file_path(directory, file):
    return os.path.join(directory, file)