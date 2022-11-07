import sys


class Triangle:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = list(a), list(b), list(c)

    def f(self, a, b):
        return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

    def __abs__(self):
        s = abs((self.b[0] - self.a[0]) * (self.c[1] - self.a[1]) - (self.c[0] - self.a[0]) *
                (self.b[1] - self.a[1]))/2
        test0 = [self.f(self.a, self.b), self.f(self.a, self.c), self.f(self.b, self.c)]
        if test0[0] + test0[1] > test0[2] and test0[0] + test0[2] > test0[1] and test0[1] + test0[2] > test0[0]:
            return s
        else:
            return 0

    def __bool__(self):
        return bool(abs(self))

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __gt__(self, other):
        return abs(self) > abs(other)

    def __contains__(self, item):
        if item.__class__ == Triangle:
            if item:
                return item.a in self and item.b in self and item.c in self
            return True
        else:
            x0, y0 = self.a
            x1, y1 = self.b
            x2, y2 = self.c
            x, y = item
            a = (x0 - x) * (y1 - y0) - (x1 - x0) * (y0 - y)
            b = (x1 - x) * (y2 - y1) - (x2 - x1) * (y1 - y)
            c = (x2 - x) * (y0 - y2) - (x0 - x2) * (y2 - y)
            return a * b >= 0 and b * c >= 0 and a * c >= 0

    def __and__(self, other):
        def g(other, self):
            return not (other.a in self and other.b in self and other.c in self) and \
                   (other.a in self or other.b in self or other.c in self)

        return bool(self) and bool(other) and (g(self, other) or g(other, self))


# r = Triangle((4, 2), (1, 0), (2, 5))
# s = Triangle((1, 3), (3, 1), (2, 5))
# t = Triangle((0, 0), (1, 3), (4, 5))
# o = Triangle((1, 1), (2, 2), (3, 5))
# print(*(f"{n}({bool(x)}):{round(abs(x), 3)}" for n, x in zip("rsto", (r, s, t, o))))
# print(f"{s < t=}, {o < t=}, {r < t=}, {r < s=}")
# print(f"{s in t=}, {o in t=}, {r in t=}")
# print(f"{r & t=}, {t & r=}, {s & r=}, {o & t=}")

exec(sys.stdin.read())
