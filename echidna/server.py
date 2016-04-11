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
import sys
import socket
import socketserver
from contextlib import contextmanager

from .request import ProxyRequestHandler
from .settings import Settings

@contextmanager
def server():
    svr = make_server()
    yield svr
    svr.shutdown()

def serve(server):
    server.serve_forever()
    
def make_server():
    settings = Settings()
    
    for server_conf in settings.servers():
        host = server_conf[0]
        port = server_conf[1]
        dhost = server_conf[2]
        dport = server_conf[3]
        
    src = (host, port)
    dst = (dhost, dport)
    
    return ProxyServer(src, dst, ProxyRequestHandler)
    
class ProxyServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, dest_address, handler_class):
        host, port = server_address
        host = socket.gethostbyname(host)
        server_address = (host, port)
        super().__init__(server_address, handler_class)
        self.dest_address = dest_address
        return
