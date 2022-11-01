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

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __gt__(self, other):
        return abs(self) > abs(other)


test1 = Triangle((0, 0), (1, 1), (2, 0))
test2 = Triangle((0, 0), (1, 2), (2, 0))
print((abs(test1)))
print((abs(test2)))
print(test1 < test2)
print(test1 > test2)
