import socket
import sys
import argparse

data_payload = 2048
backlog = 5

def echo_server(host, port):
    """A simple echo server."""
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable reuse address/port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    server_address = (host, port)
    print "Starting up echo server on %s port %s" % server_address
    sock.bind(server_address)
    # Listen to clients, backlog argument specifies the max no. of queue
    sock.listen(backlog)
    while True:
        print "Waiting to receive message"
        client, address = sock.accept()
        data = client.recv(data_payload)
        if data:
            print "Data: %s" %data
            client.send(data)
            print "Send %s bytes back to %s" %(data, address)
        client.close()


if __name__ == '__main__':
    default_host = 'localhost'
    default_port = 8080
    parser = argparse.ArgumentParser(description='Socket Client Example')
    parser.add_argument('--host', action='store', dest='host', required=False, default=default_host)
    parser.add_argument('--port', action='store', dest='port', type=int, required=False, default=default_port)
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    echo_server(host, port)