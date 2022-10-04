def sub(x, y):
    if (type(x) is list or type(x) is tuple) and (type(y) is list or type(y) is tuple):
        ans = []
        for i in x:
            if i not in y:
                ans.append(i)
        return type(x)(ans)
    else:
        return x - y


print(sub(*eval(input())))
