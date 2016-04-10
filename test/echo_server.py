"""
A simple echo server
"""

import socket
max_size = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 8081))

sock.listen(1)

while True:
    client, address = sock.accept()
    data = client.recv(max_size)
    if data:
        client.send(data)
    client.close()