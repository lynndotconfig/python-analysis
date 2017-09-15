class A(list):
	def show(self):
		print "A::show"


class B(list):
	def show(value):
		print "B::show"


class C(A):
	pass


class D(C, B):
	pass

d = D()
d.show()


for t in D.__mro__:
	print t

# ########Output ###########
# E:\code\python-analysis>python mro.py
# A::show
# <class '__main__.D'>
# <class '__main__.C'>
# <class '__main__.A'>
# <class '__main__.B'>
# <type 'list'>
# <type 'object'>