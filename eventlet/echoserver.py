# import eventlet

# def handle(client):
# 	while True:
# 		c = client.recv(1)
# 		if not c: break
# 		client.sendall(c)


# server = eventlet.listen(('0.0.0.0', 6000))
# pool = eventlet.GreenPool(1000)

# while True:
# 	new_sock, address = server.accept()
# 	pool.spawn_n(handle, new_sock)

import eventlet

def handle(fd):
	print "client connected."
	while True:
		x = fd.readline()
		if not x:
			break
		fd.write(x)
		fd.flush()
		print "echoed:", x
	print "client disconnected."

print "server socket listening on port 6000"

server = eventlet.listen(('0.0.0.0', 6000))
pool = eventlet.GreenPool()
while True:
	try:
		new_sock, address = server.accept()
		print "accepted", address
		pool.spawn_n(handle, new_sock.makefile('rw'))
	except (SystemExit, KeyboardInterrupt):
		break
