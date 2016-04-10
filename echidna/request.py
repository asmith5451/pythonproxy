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

class ProxyRequestHandler(socketserver.BaseRequestHandler):
    #
    def __init__(self, request, client_address, server):
        self.sock = create_socket()
        super().__init__(request, client_address, server)
        return
    #
    def setup(self):
        self.connect(self.sock, *self.server.dest_address)
        return super().setup()
    #
    def connect(self, sock, host, port):
        print('connecting to {}:{}'.format(host, port), file=sys.stderr)
        sock.connect(finalize_destination(host, port))
    #
    def handle(self):
        print('relaying message', file=sys.stderr)
        timeout = 0.1
        
        # accquire message
        message = bytearray()
        for chunk in network_read(self.request, timeout):
            message.extend(chunk)
       
        # relay message
        self.sock.sendall(message)

        print('relaying response', file=sys.stderr)
        
        # accquire response
        response = bytearray()
        for chunk in network_read(self.sock, timeout):
            response.extend(chunk)
        
        # relay response
        self.request.sendall(response)

        print('relay complete', file=sys.stderr)
    #
    def finish(self):
        self.sock.close()
        return super().finish()

def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def finalize_destination(host, port):
    return (socket.gethostbyname(host), port);

def network_read(sock, timeout):
    while True:
        in_wait, out_wait, err_wait = select.select([sock], [], [], timeout)
        chunk = None
        
        for s in in_wait:
           chunk = s.recv(1024) 
           yield chunk
        
        if(chunk == None or len(chunk) == 0):
            break