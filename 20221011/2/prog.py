from math import *


def scale(A, B, a, b, x):
    return (x - A) / (B - A) * (b - a) + a


w, h, a, b, f = input().split()
w = int(w)
h = int(h)
a = float(a)
b = float(b)
f = eval(f'lambda x: {f}')

X = [(x, scale(0, w + 1, a, b, x)) for x in range(w + 1)]
F = [(x[0], f(x[1])) for x in X]

y_from = min(map(lambda x: x[1], F))
y_to = max(map(lambda x: x[1], F))

F = [(i[0], round(scale(y_to, y_from, 0, h + 1, i[1]))) for i in F]

ans = [[' ' for j in range(w + 2)] for i in range(h + 2)]

for i in range(w + 1):
    ans[F[i][1]][F[i][0]] = '*'
    if i != 0:
        prev_point = F[i - 1]
        for j in range(min(F[i - 1][1], F[i][1]) + 1, max(F[i - 1][1], F[i][1])):
            ans[j][F[i - 1][0]] = '*'

for i in ans:
    print(''.join(i))
