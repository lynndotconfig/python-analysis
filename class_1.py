class A:

    def g(self, value):
        self.value = value
        print self.value


a = A()
A.g(a, 10)
