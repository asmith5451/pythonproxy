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

import socketserver
import socket

if __name__ == '__main__':
    from request import ProxyRequestHandler
    from sqlreader import SqlReader, SqlWriter
else:
    from .request import ProxyRequestHandler
    from .sqlreader import SqlReader, SqlWriter

import sys
# https://www.youtube.com/watch?v=3r8s6hrssh8

server = None


def serve():
    #import configparser
    #config = configparser.ConfigParser()
    #config.read('./server.ini')
    #host = config['proxy']['host']
    #port = int(config['proxy']['port'])
    #dhost = config['proxy']['dhost']
    #dport = int(config['proxy']['dport'])
    config = SqlReader()
    response = config.return_record()
    for thing in response:
        host = thing[0]
        port = int(thing[1])
        dhost = thing[2]
        dport = int(thing[3])
        break
    dst = (dhost, dport)
    src = (host, port)

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
