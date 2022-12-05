from numbers import Real
from functools import wraps

# class fixed(type):
#     def __new__(cls, name, bases, namespace, ndigits=3):
#         class_obj = super().__new__(cls, name, bases, namespace)
#         method_list = [func for func in dir(class_obj) if callable(getattr(class_obj, func)) and not func.startswith('__')]
#         for i in method_list:
#             class_f = getattr(class_obj, i)
# 
#             def f(*args, **kwargs):
#                 ans = class_f(*args)
#                 if isinstance(ans, Real):
#                     return round(ans, ndigits)
#                 else:
#                     return ans
# 
#             setattr(class_obj, i, f)
# 
#         return class_obj


class fixed(type):
    def __new__(cls, name, bases, namespace, ndigits=3):
        def f(fun):
            @wraps(fun)
            def wrapper(self, *a, **b):
                ans = fun(self, *a, **b)
                if isinstance(ans, Real):
                    return round(ans, ndigits)
                else:
                    return ans

            return wrapper

        class_obj = super().__new__(cls, name, bases, namespace)

        for key, value in namespace.items():
            if callable(value):
                setattr(class_obj, key, f(value))

        return class_obj



# from fractions import Fraction
# from decimal import Decimal
#
# class C(metaclass=fixed, ndigits=4):
#     def div(self, a, b):
#         return a / b
#
# print(C().div(6, 7))
# print(C().div(Fraction(6), Fraction(7)))
# print(C().div(Decimal(6), Decimal(7)))