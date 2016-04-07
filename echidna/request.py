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
        host, port = self.server.dest_address
        print('connecting to {}:{}'.format(host, port), file=sys.stderr)
        host = socket.gethostbyname(host)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        print('connected to {}:{}'.format(host, port), file=sys.stderr)
        return super().setup()
    #
    def handle(self):
        ss = select.select

        print('relaying message', file=sys.stderr)

        # relay message
        message = bytearray()
        while True:
            inwait, outwait, errwait = ss([self.request], [self.request], [])
            chunk = None
            for self.request in inwait:
                chunk = self.request.recv(1024)
                #self.sock.sendall(chunk)
                message.extend(chunk)
            if(chunk == None or len(chunk) == 0):
                break

        # send message to destination
        self.sock.sendall(message)

        print('relaying response', file=sys.stderr)

        # relay response
        message = bytearray()
        while True:
            chunk = self.sock.recv(1024)
            #self.request.sendall(chunk)
            message.extend(chunk)
            if(len(chunk) == 0):
                break

        # send response back
        self.request.sendall(message)

        print('relay complete', file=sys.stderr)
        return
    #
    def finish(self):
        self.sock.close()
        return super().finish()
