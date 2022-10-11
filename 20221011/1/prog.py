from fractions import Fraction

def f(data):
    s, w, a = data[:3]
    a = int(a)
    A = Fraction(0)
    for i in data[3:3 + a + 1]:
        A += Fraction(i) * Fraction(s) ** a
        a -= 1
    a = int(data[2])
    b = data[3 + a + 1]
    B = Fraction(0)
    for i in data[3 + a + 1 + 1:]:
        B += Fraction(i) * Fraction(s) ** b
        b -= 1
    # print(A)
    # print(B)
    if B and A/B == w:
        return True
    else:
        return False


data = list(map(Fraction, input().split(',')))

print(f(data))
