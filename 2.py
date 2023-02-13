from copy import deepcopy

graph = dict()
linerized = dict()


def check_parent(element, pretendents):
    return not any([element in it and element != it[0] for it in pretendents])


def linerize(name, bases):
    global linerized
    pretendents = [[name]]
    for b in bases:
        if b not in linerized:
            try:
                res = linerize(b, graph[b])
            except Exception:
                return False
            if not res:
                return False
        pretendents.append(linerized[b].copy())
    i = 0
    pretendents += [bases[:]]
    answer = []
    while i < len(pretendents):
        while i < len(pretendents) and len(pretendents[i]) == 0:
            i += 1
        if i == len(pretendents):
            break
        cur = pretendents[i][0]
        if check_parent(cur, pretendents):
            answer.append(cur)
            for j in range(len(pretendents)):
                if cur in pretendents[j]:
                    pretendents[j].remove(cur)
            pretendents = list(filter(lambda x: len(x) > 0, pretendents))
            i = 0
        else:
            i += 1
    pretendents = list(filter(lambda x: len(x) > 0, pretendents))
    if len(pretendents) > 0:
        return False

    linerized[name] = deepcopy(answer)

    return True


while line := input():
    words = line.split()
    if words[0] != 'class':
        continue
    end_pos = line.find("(")
    if end_pos == -1:
        end_pos = line.find(":")
    name = line[5:end_pos].strip()
    params_end_pos = line.find(")")
    if params_end_pos == -1:
        params_end_pos = line.find(":")
    bases = [x.strip() for x in line[end_pos + 1:params_end_pos].split(",")]
    bases = list(filter(lambda x: len(x) > 0, bases))
    # print(bases)
    graph[name] = bases

    if not linerize(name, bases):
        print("No")
        break
else:
    print("Yes")