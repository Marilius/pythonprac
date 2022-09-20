n = eval(input())
i = n
while i <= n + 2:
    j = n
    while j <= n + 2:
        curr = i * j
        s = 0
        while curr > 0:
            s += curr % 10
            curr //= 10
        curr = i * j

        if s == 6:
            print(i, '*', j, '= :=)', sep=' ', end=' ')
        else:
            print(i, '*', j, '=', i * j, sep=' ', end=' ')
        j += 1
    print()
    i += 1

