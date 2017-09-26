import socket
import sys

SERVER_PATH = '/tmp/python_unix_socket_server'


def run_unix_domain_socket_client():
    """Run a Unix domain socket client."""
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    # Connect the socket to the path where the server is listening.
    server_address = SERVER_PATH
    print "Connecting to %s" % server_address
    try:
        sock.connect(server_address)
    except socket.error, msg:
        print >> sys.stderr, msg
        sys.exit(1)
    try:
        message = 'This is the mesage. This will be echoed back'
        print "Sendiing [%s]" % message
        sock.sendall(message)
        amount_recevied = 0
        amount_expected = len(message)

        while amount_recevied < amount_expected:
            data = sock.recv(16)
            amount_recevied += len(data)
            print >> sys.stderr, "Recevied [%s]" % data
    finally:
        print "Closing client"
        sock.close()

if __name__ == '__main__':
    run_unix_domain_socket_client()
