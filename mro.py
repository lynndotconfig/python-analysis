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