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
import logging
import sys
import socketserver
import socket
import select

from contextlib import contextmanager

#
class ProxyRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        with standard_socket(self.server.dest_address) as sock:
            # relay message
            relay(self.request, sock)
            
            # relay response
            relay(sock, self.request)

@contextmanager
def standard_socket(address):
    # setup
    sock = socket.create_connection(address)
    yield sock
    
    # teardown
    sock.close()

#
def relay(src, dst):
    for chunk in xml_read(src):
        dst.sendall(chunk)

#
def xml_read(sock, timeout = 0.01):
    # TODO: tune timeout for real-world application
    # TODO: build logic that handles XML data instead of guessing that the
    # connection is over by whether data was recieved.
    while True:
        in_wait, out_wait, err_wait = select.select([sock], [], [], timeout)
        chunk = None
        
        for s in in_wait:
           chunk = s.recv(1024) 
           yield chunk
        
        if(chunk == None or len(chunk) == 0):
            break
