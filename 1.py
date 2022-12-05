d = dict()
linerized = dict()


def check_parent(element, arr):
    return not any(element in i and element != i[0] for i in arr)


def linerize(name, bases):
    parents = [[name]]
    for b in bases:
        if b not in linerized:
            if b in d:
                res = linerize(b, d[b])
            else:
                return False
            if not res:
                return False
        parents.append(linerized[b].copy())
    i = 0
    parents.append(bases.copy())
    answer = []
    while i < len(parents):
        while not len(parents[i]):
            i += 1
            if i == len(parents):
                break
        if i == len(parents):
            break
        cur = parents[i][0]
        if check_parent(cur, parents):
            answer.append(cur)
            for j in range(len(parents)):
                if cur in parents[j]:
                    parents[j].remove(cur)
            parents = list(filter(None, parents))
            i = 0
        else:
            i += 1
    parents = list(filter(None, parents))

    if len(parents):
        return False

    linerized[name] = answer.copy()

    return True


while line := input():
    words = line.split()
    if words[0] != 'class':
        continue

    start = line.find("(")
    if start == -1:
        start = line.find(":")

    end = line.find(")")
    if end == -1:
        end = line.find(":")

    params = map(str.strip, line[start + 1:end].split(","))
    params = list(filter(None, params))
    # print(params)

    name = line[5:start].strip()
    d[name] = params

    print(d)

    if not linerize(name, params):
        print("No")
        break
else:
    print("Yes")


'''

class A:
    B = 0
class B(A): pass
class C(A, B):
    A = B = C = 5

'''