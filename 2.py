from inspect import get_annotations, getfullargspec, formatargspec
from types import GenericAlias
from functools import wraps


class init(type):
    def __init__(cls, name, bases, namespace, *args, **kwargs):
        print(get_annotations(cls))
        print(dir(cls))
        for name in dir(cls):
            func = getattr(cls, name)
            if callable(func):
                print(func)
                params = getfullargspec(func)
                print(params)
                # print(get_annotations(func))
                # def
                # @wraps(func)
                # def f(*a, **b):
                #     pass

        for attr_name, annotation_type in get_annotations(cls).items():
            print(1)
            if not hasattr(cls, attr_name):
                print('!!!')
            else:
                print(attr_name)
                # attr = getattr(cls, attr_name)

            # if not callable(attr):
            #     attr_type = type(attr)
            #     if type(annotation_type) == GenericAlias:
            #         annotation_type = annotation_type.__origin__
            #     if attr_type is not annotation_type and not issubclass(attr_type, annotation_type):
            #         return False

        # setattr(cls, data.__name__, data)
        super().__init__(name, bases, namespace)


class C(metaclass=init):
    def __init__(self, var: int, rng: range, lst: list[int], defined: str = "defined"):
        self.data = f"{var}/{rng}/{lst}/{defined}"


for c in [C(var=1, rng=range(3), lst=[1], defined='sss')]:
    print(c.data)
