import sys


def fib(m, n):
    a0 = 1
    a1 = 1
    for i in range(n+1):
        if m <= i <= n:
            yield a0
        a0, a1 = a1, a0 + a1


# print(*list(fib(2, 4)), sep=', ')

exec(sys.stdin.read())
