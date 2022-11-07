import sys


class Omnibus:
    _r = {}
    # r = 0

    # def __init__(self):
        # Omnibus.r += 1

    def __setattr__(self, key, value):
        self._r.setdefault(key, set())
        self._r[key].add(self)

        # Omnibus._r[key] += 1

    def __getattr__(self, item):
        # print(Omnibus.r)
        # return Omnibus._r[item]
        return len(self._r[item])

    def __delattr__(self, item):
        # if Omnibus._r[item]:
        #     Omnibus._r[item] -= 1
        if self in self._r.get(item, set()):
            self._r[item] -= {self}


# a, b, c = Omnibus(), Omnibus(), Omnibus()
# del a.random
# a.i = a.j = a.k = True
# b.j = b.k = b.n = False
# c.k = c.n = c.m = hex
# print(a.i, a.j, a.k, b.j, b.k, b.n, c.k, c.n, c.m)
# del a.k, b.n, c.m
# print(a.i, a.j, b.j, b.k, c.k, c.n)
# del a.k, c.m
# print(a.i, a.j, b.j, b.k, c.k, c.n)
# a.k = b.i = c.m = 777
# print(a.i, a.j, a.k, b.j, b.k, c.k, c.n, c.m)

exec(sys.stdin.read())
