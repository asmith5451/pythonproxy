import socket
import sys

# settings
# bind_address = socket.gethostbyname(socket.getfqdn())
bind_address = socket.gethostbyname('10.224.16.204')
bind_port = 10000


# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
relay_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the port
print('starting up on {} port {}'.format(bind_address, bind_port), file=sys.stderr)
sock.bind((bind_address, bind_port))
relay_sock.bind((bind_address, bind_port))


# put the socket into server mode
sock.listen(1)

while True:
    # wait for a connection
    print('waiting for a connection', file=sys.stderr)
    connection, client_address = sock.accept()
    try:
        # recieve data in small chunks and retransmit it
        print('connection from {}'.format(client_address), file=sys.stderr)
        while True:
            data = connection.recv(16)
            print('recieved "{}"'.format(data.decode('utf-8')))
            if data:
                print('sending data back to client')
                #  relay = socket.create_connection('10.224.5.60', source_address='10.224.16.204')
                relay_sock.sendto(data, ('10.224.5.60', 9080))
                # connection.sendall(data)

            else:
                print('no more data from {}'.format(client_address))
                break
    except UnicodeDecodeError:
        # clean up the connection anyway
        connection.close()
    finally:
        # clean up the connection
        connection.close()
