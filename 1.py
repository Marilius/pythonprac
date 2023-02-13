d, dd = dict(), dict()


def f(class_name, params):
    global d, dd
    arr = [[class_name]]
    for curr in params:
        if curr not in dd:
            try:
                if not f(curr, d[curr]):
                    return False
            except Exception:
                return False
        arr.append(dd[curr].copy())
    arr += [params.copy()]
    ans = []
    i = 0
    while i < len(arr):
        while i < len(arr) and not arr[i]:
            i += 1
        if i == len(arr):
            break

        curr = arr[i][0]

        flag = True
        for j in arr:
            if curr in j and curr != j[0]:
                flag = False
                i += 1
                break

        if flag:
            ans.append(curr)
            for j in range(len(arr)):
                if curr in arr[j]:
                    arr[j].remove(curr)
            arr = list(filter(None, arr))
            i = 0

    arr = list(filter(None, arr))
    if arr:
        return False

    dd[class_name] = ans.copy()

    return True


while curr := input():
    if curr[:5] != 'class':
        continue
    curr = curr[5:].replace(' ', '')
    end_pos, params_end_pos = curr.find('('), curr.find(')')
    if end_pos == -1:
        end_pos = curr.find(':')
    if params_end_pos == -1:
        params_end_pos = curr.find(':')
    class_name = curr[:end_pos]
    params = list(filter(None, curr[end_pos + 1:params_end_pos].split(',')))
    # print(params)

    d[class_name] = params

    if not f(class_name, params):
        print('No')
        break
else:
    print('Yes')
