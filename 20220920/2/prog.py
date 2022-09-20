s = 0
while True:
    n = eval(input())
    if n <= 0:
        print(n)
        break
    s += n
    if s > 21:
        print(s)
        break
