import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bind_address = socket.gethostbyname(socket.getfqdn())
bind_port = 10000

print('connecting to server {} on port {}'.format(bind_address, bind_port),
      file=sys.stderr)

sock.connect((bind_address, bind_port))

try:
    message = 'This is the message. It will be repeated.'
    print('sending "{}"'.format(message), file=sys.stderr)
    sock.sendall(message.encode('utf-8'))

    amount_recieved = 0
    amount_expected = len(message)

    while amount_recieved < amount_expected:
        data = sock.recv(16)
        amount_recieved += len(data)
        print('recieved "{}"'.format(data.decode('utf-8')), file=sys.stderr)

finally:
    print('closing socket', file=sys.stderr)
    sock.close()
