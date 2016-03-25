import logging
import sys
import socketserver

class ProxyRequestHandler(socketserver.BaseRequestHandler):
    # 
    def __init(self, request, client_address, server):
        super(ProxyRequestHandler, self).__init__(request, client_address, server)
        return
    # 
    def setup(self):
        return super(ProxyRequestHandler, self).setup()
    #
    def handle(self):
        # echo back to the client
        data = self.request.recv(1024)
        self.request.send(data)
        return
    #
    def finish(self):
        return super(ProxyRequestHandler, self).finish()
