a = eval(input())
n = len(a)
m1 = [a] + [eval(input()) for i in range(1, n)]

m2 = [eval(input()) for i in range(n)]

ans = [[0 for j in range(n)] for i in range(n)]

for i in range(n):
    for j in range(n):
        for k in range(n):
            ans[i][j] += m1[i][k] * m2[k][j]

for i in range(n):
    print(*ans[i], sep=',')
