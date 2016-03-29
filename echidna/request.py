import logging
import sys
import socketserver
import socket

class ProxyRequestHandler(socketserver.BaseRequestHandler):
    # 
    def __init__(self, request, client_address, server):
        super(ProxyRequestHandler, self).__init__(request, client_address, server)
        return
    # 
    def setup(self):
        host, port = self.server.dest_address
        print('connecting to {}:{}'.format(host, port), file=sys.stderr)
        host = socket.gethostbyname(host)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        print('connected to {}:{}'.format(host, port), file=sys.stderr)
        return super(ProxyRequestHandler, self).setup()
    #
    def handle(self):
        print('transmitting data', file=sys.stderr)
        while True:
            message = self.request.recv(1024)
            self.sock.sendall(message)
            if(len(message) < 1024):
                break
        print('recieving data', file=sys.stderr)
        while True:
            message = self.sock.recv(1024)
            self.request.sendall(message)
            if(len(message) < 1024):
                break
        return
    #
    def finish(self):
        self.sock.close()
        return super(ProxyRequestHandler, self).finish()
