import sys


def objcount(some_class):
    class count(some_class):
        some_class.counter = 0

        def __init__(self, *args, **kwargs):
            some_class.counter += 1

        def __del__(self, *args, **kwargs):
            some_class.counter -= 1

    return count


@objcount
class C:
    pass


# c, d, e = C(bool), C(int), C(list)
# a = [C(str) for i in range(100)]
# print(C.counter)
# c = 100500
# print(C.counter)

exec(sys.stdin.read())
