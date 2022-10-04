from math import *


def Calc(s, t, u):
    def f1(x):
        return eval(s)

    def f2(x):
        return eval(t)

    def f(x, y):
        return eval(u)

    def ans(x):
        return f(f1(x), f2(x))
    return ans


a, b, c = eval(input())
x = eval(input())
print(Calc(a, b, c)(x))
