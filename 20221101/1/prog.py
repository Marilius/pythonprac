from collections import defaultdict


class Omnibus:
    r = defaultdict(lambda: 0)
    # r = 0

    # def __init__(self):
        # Omnibus.r += 1

    def __setattr__(self, key, value):
        # self.__dict__[f'_{key}'] = value
        Omnibus.r[key] += 1

    def __getattr__(self, item):
        # print(Omnibus.r)
        return Omnibus.r[item]

    def __delattr__(self, item):
        Omnibus.r[item] -= 1


# a = Omnibus()
# a.a = 1
# print(a.a)
# # print(a.r)
# a = Omnibus()
# a.a = 1
# print(a.a)
#
# b = Omnibus()
# b.a = 1
# print(b.a)
# # print(Omnibus.r)
# del b.a
# print(b.a)