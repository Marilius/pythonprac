class InvalidInput(Exception):
    pass


class BadTriangle(Exception):
    pass


def f(x, y):
    return (x**2 + y**2)**0.5


def triangleSquare(data):
    try:
        a, b, c = eval(data)
        x1, y1 = a
        x2, y2 = b
        x3, y3 = c
    except Exception:
        raise InvalidInput

    a, b, c = f(x1 - x2, y1 - y2), f(x2 - x3, y2 - y3), f(x3 - x1, y3 - y1)
    # if (a > b + c) and (b > a + c) and (c > a + b):
    if max(a, b, c) < min(a + b, b + c, c + a):
        return abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) * 0.5
    else:
        raise BadTriangle


while True:
    s = input()
    try:
        ans = triangleSquare(s)

    except InvalidInput:
        print("InvalidInput")
        continue
    except BadTriangle:
        print("Not a triangle")
        continue

    print(ans)
    break
