import sys
from itertools import islice, tee


def slide(seq, n):
    while True:
        s, seq = tee(seq)
        s = list(s)
        if not s:
            return
        yield from islice(s, n)
        next(seq)


print(*list(slide('help me plz', 1)))
# print(*list(slide(range(5), 3)))
# print(list(islice('abcdef', 10)))

exec(sys.stdin.read())


