import argparse
import socket
import sys


HOST = 'localhost'
BUFSIZE = 1024

def echo_client(port, host=HOST):
    """Echo client using ipv6."""
    for res in socket.getaddrinfo(
        host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            sock = socket.socket(af, socktype, proto)
        except socket.error, err:
            print "Error: %s" % err
        try:
            sock.connect(sa)
            print "Client connecting to %s:%s" % (host,port)
        except socket.error, msg:
            sock.close()
            continue
    if sock is None:
        print 'Failed to open socket.!'
        sys.exit(1)
    msg = 'Hello from ipv6 client.'
    print 'Send data to server: [%s]' % msg
    sock.send(msg)
    while True:
        data = sock.recv(BUFSIZE)
        print "Recevied data from the server: [%s] " % data
        if not data: break
    sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ipv6 Socket server Example.')
    parser.add_argument('--port', action='store', dest='port', type=int, default=8081)
    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)
