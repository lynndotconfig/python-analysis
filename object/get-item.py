"""object has no dict like method."""
class Vhost(object):

	def __init__(self, name, permission):
		self.name = name
		self.permission = permission


if __name__ == '__main__':

	vhost1 = {
		"name": "test2",
		"permissions": "partily"
	}

	print "name:", vhost1["name"]
	print "permissions:", vhost1["permissions"]

	vhost = Vhost("test1", "all")
	print "name:", vhost["name"]
	print "permssion", vhost["permssion"]
