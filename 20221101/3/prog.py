import sys
from math import log


class Grange:
    def __init__(self, b0, q, bn):
        self.b0 = b0
        self.q = q
        self.bn = bn

    def __len__(self):
        n = int((self.bn / self.b0))
        if n == 1:
            return 0
        else:
            return int(log(n - 1, self.q)) + 1

    def __getitem__(self, it):
        if type(it) == slice:
            return Grange(it.start, self.q**it.step if it.step is not None else self.q, it.stop)
        if type(it) == int:
            return self.b0 * self.q**it

    def __iter__(self):
        if len(self):
            prev = self.b0
            yield prev
            for i in range(len(self) - 1):
                prev *= self.q
                yield prev

    def __str__(self):
        return f"grange({self.b0}, {self.q}, {self.bn})"

    def __repr__(self):
        return self.__str__()


# f, g, h = Grange(1, 3, 1048575), Grange(1, 3, 1048576), Grange(1, 3, 1048577)
# o, e = Grange(1, 2, 2), Grange(100, 11, 200)
# print(f"{f=}, {g=}, {h=}")
# print(f"{list(o)}({not(o)}), {list(e)}({not(e)})")
# print(f"{len(f)=}, {len(g)=}, {len(h)=}")
# print(f"{len(list(f))=}, {len(list(g))=}, {len(list(h))=}")
# print(f"{f[0]=}, {h[24]=}")
# a, b = f[3:10], h[3:100:2]
# print(f"{a=}, {a[5]=}")
# print(f"{b=}, {b[5]=}, {list(b)=}")

exec(sys.stdin.read())
