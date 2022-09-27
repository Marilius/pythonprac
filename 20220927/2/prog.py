a = list(eval(input()))

f = True
while f:
    f = False
    for i in range(1, len(a)):
        if a[i - 1] ** 2 % 100 > a[i] ** 2 % 100:
            f = True
            a[i - 1], a[i] = a[i], a[i - 1]

print(a)
