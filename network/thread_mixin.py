"""Not supoort in Windows, Because of 'os.fork()' not supported in windows."""
import os
import socket
import threading
import SocketServer

SERVER_HOST = 'localhost'
SERVER_PORT = 0  # Tell the kernel to pick up a port dynamically
BUF_SIZE = 1024

def client(ip, port, message):
    """A client to test threading mixin server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    try:
      sock.sendall(message)
      response = sock.recv(BUF_SIZE)
      print "Client received: %s" % response
    finally:
        sock.close()


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    """An example of threaded TCP request handler."""
    def handle(self):
        data = self.request.recv(1024)
        current_thread = threading.current_thread()
        response = "%s: %s" % (current_thread.name, data)
        self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """Nothing to add here, inherit everything necessary from parents"""
    pass


def main():
    # Launch the server
    server = ThreadedTCPServer((SERVER_HOST, SERVER_PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print 'Server loop running PID: %s' %os.getpid()

    # Launch the client
    client(ip, port, 'Hello from client 1')
    client(ip, port, 'Hello from client 2')
    client(ip, port, 'Hello from client 3')
    
    # Clean them up
    server.shutdown()


if __name__ == '__main__':
  main()