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
        super().__init__(request, client_address, server)
        return
    #
    def setup(self):
        self.sock = create_socket()
        self.connect(self.sock, *self.server.dest_address)
        return super().setup()
    #
    def connect(self, sock, host, port):
        sock.connect(finalize_destination(host, port))
    #
    def handle(self):
        # TODO: tune timeout for real-world application
        timeout = 0.1
        
        # relay message
        message = proxy_readall(self.request, timeout)
        self.sock.sendall(message)
        
        # relay response
        response = proxy_readall(self.sock, timeout)
        self.request.sendall(response)
    #
    def finish(self):
        self.sock.close()
        return super().finish()

def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def finalize_destination(host, port):
    return (socket.gethostbyname(host), port);

def proxy_readall(sock, timeout):
    message = bytearray()
    for chunk in network_read(sock, timeout):
        message.extend(chunk)
    return message

def network_read(sock, timeout):
    # TODO: build logic that handles XML data instead of guessing that the
    # connection is over by weather data was recieved.
    while True:
        in_wait, out_wait, err_wait = select.select([sock], [], [], timeout)
        chunk = None
        
        for s in in_wait:
           chunk = s.recv(1024) 
           yield chunk
        
        if(chunk == None or len(chunk) == 0):
            break
