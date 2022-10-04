def Pareto(*x):
    ans = []

    for i in range(len(x)):
        f = True
        for j in range(len(x)):
            if i != j:
                if x[i][0] <=  x[j][0] and x[i][1] <=  x[j][1]:
                    if x[i][0] < x[j][0] or x[i][1] < x[j][1]:
                        f = False
                        break

        if f:
            ans.append(x[i])

    return tuple(ans)


print(Pareto(*eval(input())))
