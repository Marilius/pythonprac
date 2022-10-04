def rec(a, s):
    n = int(len(s)/2)
    if len(s) == 1 and a != s[0]:
        return False
    if a == s[n]:
        return True
    elif a > s[n]:
        return rec(a, s[n:])
    else:
        return rec(a, s[:n])


print(rec(*eval(input())))
