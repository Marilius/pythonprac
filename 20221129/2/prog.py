from inspect import get_annotations
from types import GenericAlias
import sys


class check(type):
    def __init__(cls, name, bases, namespace, *args, **kwargs):
        def check_annotations(self):
            for attr_name, annotation_type in get_annotations(self.__class__).items():
                if not hasattr(self, attr_name):
                    return False
                attr = getattr(self, attr_name)

                if not callable(attr):
                    attr_type = type(attr)
                    if type(annotation_type) == GenericAlias:
                        annotation_type = annotation_type.__origin__
                    if attr_type is not annotation_type and not issubclass(attr_type, annotation_type):
                        return False
            return True

        setattr(cls, check_annotations.__name__, check_annotations)
        super().__init__(name, bases, namespace)


# class C(metaclass=check):
#     B: float
#
#
# c = C()
# print(c.check_annotations())
# c.B = 12.0
# print(c.check_annotations())
# c.B = [100500, 42, False]
# print(c.check_annotations())
# c.B = 100/111
# print(c.check_annotations())
# c.B = C()
# print(c.check_annotations())

exec(sys.stdin.read())
