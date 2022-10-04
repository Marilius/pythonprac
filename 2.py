# def p(x):
#     global tree, ans
#     start = 0
#     for i in range(1, n + 1):
#         # print(i)
#         if tree[i]['p'] is None:
#             start = i
#             break
#     x =
#     # print('!!!!', x)
#     if 'l' in tree[x].keys():
#         if tree[x]['l'] is not None:
#             p(tree[x]['l'])
#
#     print(x, end=' ')
#
#     if 'r' in tree[x]:
#         if tree[x]['r'] is not None:
#             p(tree[x]['r'])
#
#
# n, q = map(int, input().split())
# changes = list(map(int, input().split()))
#
# tree = dict()
# tree[1] = dict()
# tree[1]['p'] = None
#
# for i in range(1, n+1):
#     if 3*i <= n:
#         tree[i]['l'] = 3*i
#         tree[3*i] = dict()
#         tree[3 * i]['p'] = i
#     if 3*i + 1 <= n:
#         tree[i]['r'] = 3*i + 1
#         tree[3*i + 1] = dict()
#         tree[3*i + 1]['p'] = i
#
#
# # print(tree)
#
# for v in changes:
#     print(v)
#     p(tree)
#     if tree[v]['p'] is None:
#         continue
#
#     parent = tree[v]['p']
#
#     if tree[parent]['p'] is not None:
#         pp = tree[parent]['p']
#         if parent == tree[pp]['l']:
#             tree[pp]['l'] = v
#             tree[v]['p'] = pp
#         else:
#             tree[pp]['r'] = v
#             tree[v]['p'] = pp
#
#     if tree[parent]['l'] == v:
#         tree[v]['l'] = parent
#         tree[parent]['p'] = v
#         tree[parent]['l'] = tree[v]['l']
#         tree[tree[v]['l']]['p'] = tree[parent]
#     else:
#         tree[v]['r'] = parent
#         tree[parent]['p'] = v
#         tree[parent]['r'] = tree[v]['r']
#         tree[tree[v]['r']]['p'] = tree[parent]
#         pass
#
#
#
# ans = []
#
#
# print(tree)
# p(tree)
#
# ans_str = ''.join(map(str, ans))
# print(ans_str)
