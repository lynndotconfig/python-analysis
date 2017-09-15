import socket
from binascii import hexlify

import sys
import argparse

host_name = socket.gethostname()
print host_name


ip_address = socket.gethostbyname(host_name)
print ip_address


remote_host = 'www.baidu.com'
print socket.gethostbyname(remote_host)


def convert_ip4_address():
    for ip_addr in ['127.0.0.1', '10.3.16.128']:
        packed_ip_addr = socket.inet_aton(ip_addr)
        unpacked_ip_addr = socket.inet_ntoa(packed_ip_addr)
        print "IP Address: %s => Packed: %s, Unpacked: %s" %(ip_addr, hexlify(packed_ip_addr), unpacked_ip_addr)


def find_service_name():
    protocalname = 'tcp'
    for port in [80, 25]:
        print "Port: %s => service name: %s" %(port, socket.getservbyport(port, protocalname))
    print "Port: %s => service name: %s" % (53, socket.getservbyport(53, 'udp'))


def convert_integer():
    data = 1234
    # 32-bit
    print "Original: %s => Long host by order: %s, Network byte order: %s" %(data, socket.ntohl(data), socket.htonl(data))
    # 16-bit
    print "Original: %s => Short host byte order: %s, Network byte order: %s" %(data, socket.ntohs(data), socket.htons(data))


def test_socket_timeout():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Default socket timeout: %s" %s.gettimeout()
    s.settimeout(100)
    print "Current socket timeout: %s" %s.gettimeout()

def socket_errors():
    # run 'python network.py --host=127.0.0.1 --port=80 --file=socket_errors.py'
    # setup argument parsing
    parser = argparse.ArgumentParser(description='Socket Error Example')
    parser.add_argument('--host', action='store', dest='host', required=False)
    parser.add_argument('--port', action='store', dest='port', type=int, required=False)
    parser.add_argument('--file', action='store', dest='file', required=False)
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    filename = given_args.file

    # First try-except block -- create socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, e:
        print "Error creating socket: %s" % e
        sys.exit(1)

    # Second try-block -- connect to host
    try:
        s.connect((host, port))
    except socket.gaierror, e:
        print "Address-related error connecting to server: %s" % e
        sys.exit(1)
    except socket.error, e:
        print "Connection error: %s" % e
        sys.exit(1)

    # Third try-except block -- sending data

    try:
        s.sendall('GET %s HTTP/1.0\r\n\r\n' % filename)
    except socket.error, e:
        print 'Error sending data: %s' %e
        sys.exit(1)

    while True:
        # Fourth try-except block -- waiting to receive data from remote host
        try:
            buf = s.recv(2048)
        except socket.error, e:
            print 'Error receiving data: %s' % e
            sys.exit(1)
        if not len(buf):
            break
        sys.stdout.write(buf)


def modify_buff_size():
    SEND_BUF_SIZE = 4096
    RECV_BUF_SIZE = 4096

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get the size of the socket's send buffer
    bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print 'Buffer size [Before]: %d' % bufsize

    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)
    bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print 'Buffer size [After]: %d' % bufsize

if __name__ == '__main__':
    # convert_ip4_address()
    # find_service_name()
    # convert_integer()
    # test_socket_timeout()
    # socket_errors()
    modify_buff_size()