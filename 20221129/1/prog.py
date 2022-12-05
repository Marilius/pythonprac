import sys
from functools import wraps


class dump(type):
    def __init__(cls, name, bases, namespace, **kwargs):
        def f(fun):
            @wraps(fun)
            def wrapper(self, *a, **b):
                print(f'{wrapper.__name__}: {a}, {b}')
                return fun(self, *a, **b)

            return wrapper

        for key, value in namespace.items():
            if callable(value):
                setattr(cls, key, f(value))

        super().__init__(name, bases, namespace)


# class C(metaclass=dump):
#     def __init__(self, a, **b):
#         self.a = self.f69(a)
#
#     @staticmethod
#     def f69(x, *a):
#         return '69'
#
#     def add(self, *a):
#         self.a += self.f69(a)
#         return self.a
#
#
# c = C(10)
# print(c.f69('золото'))
# print(c.f69('курячий'))

exec(sys.stdin.read())
