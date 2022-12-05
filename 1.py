def statcounter():
    pass


stat = statcounter()
stats = next(stat)

@stat.send
def f1(a): return a+1

@stat.send
def f2(a, b): return f1(a)+f1(b)

print(f1(f2(2,3)+f2(5,6)))
print(*((f.__name__, c) for f, c in stats.items()))