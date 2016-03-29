import socketserver
import socket
from .request import ProxyRequestHandler
import sys
# https://www.youtube.com/watch?v=3r8s6hrssh8

server = None
def serve():
    import configparser
    config = configparser.ConfigParser()
    config.read('./server.ini')
    host = config['proxy']['host']
    port = int(config['proxy']['port'])
    dhost = config['proxy']['dhost']
    dport = int(config['proxy']['dport'])
    src = (host, port)
    dst = (dhost, dport)

    global server
    print("setup called", file=sys.stderr)
    server = ProxyServer(src, dst, ProxyRequestHandler)
    server.serve_forever()

def teardown():
    print("teardown called", file=sys.stderr)
    server.shutdown()

def reload_config():
    print("reload called", file=sys.stderr)
    server.shutdown()
    server.serve_forever()

class ProxyServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, dest_address, handler_class):
        host, port = server_address
        host = socket.gethostbyname(host)
        server_address = (host, port)
        super().__init__(server_address, handler_class)
        self.dest_address = dest_address
        return

if __name__ == '__main__':
    try:
        serve()
    except KeyboardInterrupt:
        teardown()
