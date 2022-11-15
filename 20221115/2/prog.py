import sys


class Num():
    def __init__(self):
        self.num = 0

    def __get__(self, instance, owner):
        if 'num' in instance.__dict__:
            return instance.__dict__['num']
        else:
            return self.__dict__['num']

    def __set__(self, instance, value):
        if hasattr(value, 'real'):
            instance.__dict__['num'] = value
        elif hasattr(value, '__len__'):
            instance.__dict__['num'] = len(value)


# class C:
#     num = Num()
#
#
# a = C()
# a.num = 'kakaska'
# print(a.num)
# print(C().num)
# c, d = C(), C()
# c.num = d.num = 6
# print(c.num+d.num)
# c.num = "lolkek_test_test"
# print(c.num+d.num)
# d.num = range(100, 500, 23)
# print(c.num+d.num)

exec(sys.stdin.read())
