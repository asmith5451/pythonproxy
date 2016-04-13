import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bind_address = socket.gethostbyname(socket.getfqdn())
bind_port = 8082

print('connecting to server {} on port {}'.format(bind_address, bind_port),
      file=sys.stderr)

sock.connect((bind_address, bind_port))

try:
    message = 'GET / HTTP/1.0\nhost: www.example.com\n\n'
    print('sending "{}"'.format(message), file=sys.stderr)
    sock.sendall(message.encode('utf-8'))

    # recieve message to relay
    message = bytearray()
    print('receiving data', file=sys.stderr)
    while True:
        chunk = sock.recv(1024)
        if(len(chunk) == 0):
            break
        message.extend(chunk)

    print('recieved "{}"'.format(message.decode('utf-8')), file=sys.stderr)

finally:
    print('closing socket', file=sys.stderr)
    sock.close()
