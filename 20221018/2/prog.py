import math

namespace = dict()
i = 0
j = 1
while True:
    curr = input().strip()
    i += 1
    if curr[0] == ':':
        j += 1
        curr = curr[1:].split()
        # namespace[curr[0]] = eval(f'lambda {",".join(curr[1:-1])}: {curr[-1]}')
        namespace[curr[0]] = (curr[1:-1], curr[-1])
    else:
        curr = curr.split()
        if curr[0] == 'quit':
            s = eval(' '.join(curr[1:]).format(j, i))
            print(s)
            break
        else:
            var = curr[1:]
            ctx = {namespace[curr[0]][0][i]: eval(var[i]) for i in range(len(var))} if len(var) else {}
            print(eval(namespace[curr[0]][1], ctx, vars(math)))

