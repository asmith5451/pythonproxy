import socketserver
import request

class ProxyServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, handler_class=request.ProxyRequestHandler):
        socketserver.TCPServer.__init__(self, server_address, handler_class)
        return
    def server_activate(self):
        socketserver.TCPServer.server_activate(self)
        return
    def serve_forever(self, poll_interval=0.5):
        socketserver.TCPServer.serve_forever(self, poll_interval)
        return
    def handle_request(self):
        return socketserver.TCPServer.handle_request(self)
    def verify_request(self, request, client_address):
        return socketserver.TCPServer.verify_request(self, request, client_address)
    def process_request(self, request, client_address):
        return socketserver.TCPServer.process_request(self, request, client_address)
    def server_close(self):
        return socketserver.TCPServer.server_close(self)
    def finish_request(self, request, client_address):
        return socketserver.TCPServer.finish_request(self, request, client_address)
    def close_request(self, request_address):
        return socketserver.TCPServer.close_request(self, request_address)
    def shutdown(self):
        return socketserver.TCPServer.shutdown(self)

if __name__ == '__main__':
    import sys
    import socket

    if len(sys.argv) != 3:
        print('usage: python server2.py [host] [port]', file=sys.stderr)
        sys.exit()

    address = sys.argv[1]
    port = int(sys.argv[2])

    address = (socket.gethostbyname(address), port)
    server = ProxyServer(address, request.ProxyRequestHandler)
    ip, port = server.server_address

    server.serve_forever()
