# a = 1


# def f():
# 	a = 2

# 	def g():
# 		print a
# 	return g

# func = f()
# func()

# a = 1

# def g():
# 	print a

# def f():
# 	global a
# 	print a
# 	a = 2
# 	print a

# g()
# f()

# # output
# 1
# 1
# 2

import sys

msg = 'hello world'

class A(object):

	def set(self, name):
		self.name = name

	def show(self, show_name):
		if show_name:
			print self.name
		else:
			print msg

a = A()
a.set('python')
a.show(True)