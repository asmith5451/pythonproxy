import logging
import sys
import socketserver

class ProxyRequestHandler(socketserver.BaseRequestHandler):
    # 
    def __init(self, request, client_address, server):
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return
    # 
    def setup(self):
        return socketserver.BaseRequestHandler.setup(self)
    #
    def handle(self):
        # echo back to the client
        data = self.request.recv(1024)
        self.request.send(data)
        return
    #
    def finish(self):
        return socketserver.BaseRequestHandler.finish(self)
