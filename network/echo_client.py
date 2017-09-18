import socket
import sys
import argparse

def echo_client(host, port):
    """"A simple echo client."""
    # Create a socket client
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connetion the socket to the server.
    server_addr = (host, port)
    print "Conectiong to server: %s:%s" %(server_addr)
    sock.connect(server_addr)

    # Send data
    try:
        msg = "Test message. This will be echoed."
        print "Send message: %s" %(msg)
        sock.sendall(msg)

        # Look for the response
        amount_received = 0
        amount_expected = len(msg)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print "Received: %s" % data
    except socket.errno, e:
        print "Socket Error: %s" % str(e)
    except Exception, e:
        print "Other ecxeption: %s" % str(e)
    finally:
      print "Closing connection to the server."
      sock.close()


if __name__ == '__main__':
    default_host = 'localhost'
    default_port = 8080
    parser = argparse.ArgumentParser(description='Socket Client Example')
    parser.add_argument('--host', action='store', dest='host', required=False, default=default_host)
    parser.add_argument('--port', action='store', dest='port', type=int, required=False, default=default_port)
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    echo_client(host, port)