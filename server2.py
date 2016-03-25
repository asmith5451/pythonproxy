import socketserver
import request
# https://www.youtube.com/watch?v=3r8s6hrssh8

class ProxyServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, dest_address, handler_class):
        super(ProxyServer, self).__init__(server_address, handler_class)
        self.dest_address = dest_address
        return
    def server_activate(self):
        super(ProxyServer, self).server_activate()
        return
    def serve_forever(self, poll_interval=0.5):
        super(ProxyServer, self).serve_forever(poll_interval)
        return
    def handle_request(self):
        return super(ProxyServer, self).handle_request()
    def verify_request(self, request, client_address):
        return super(ProxyServer, self).verify_request(request, client_address)
    def process_request(self, request, client_address):
        return super(ProxyServer, self).process_request(request, client_address)
    def server_close(self):
        return super(ProxyServer, self).server_close()
    def finish_request(self, request, client_address):
        return super(ProxyServer, self).finish_request(request, client_address)
    def close_request(self, request_address):
        return super(ProxyServer, self).close_request(request_address)
    def shutdown(self):
        return super(ProxyServer, self).shutdown()

if __name__ == '__main__':
    import sys
    import socket
    import configparser
    config = configparser.ConfigParser()
    config.read('server2.ini')

    host = config['proxy']['host']
    port = int(config['proxy']['port'])
    dhost = config['proxy']['dhost']
    dport = int(config['proxy']['dport'])

    src = (socket.gethostbyname(host), port)
    dst = (dhost, dport)
    server = ProxyServer(src, dst, request.ProxyRequestHandler)

    server.serve_forever()
