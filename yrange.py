class yrange:

    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return i
        else:
            raise StopIteration()


class zrange:

    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return zrange_iter(self.n)


class zrange_iter:

    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return i
        raise StopIteration()


class zrange_reverse:

    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        if self.i > 0:
            i = self.i
            self.i -= 1
            return i
        raise StopIteration()
