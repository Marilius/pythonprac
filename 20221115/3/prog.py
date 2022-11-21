import sys
import string


class Alpha:
    __slots__ = list(string.ascii_lowercase)

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self):
        ans = []
        for key in self.__slots__:
            if hasattr(self, key):
                ans.append(f'{key}: {getattr(self, key)}')
        return ', '.join(ans)


class AlphaQ:
    def __init__(self, **kwargs):
        for key in kwargs:
            if key in list(string.ascii_lowercase):
                setattr(self, key, kwargs[key])
            else:
                raise AttributeError

    def __setattr__(self, key, value):
        if key in list(string.ascii_lowercase):
            self.__dict__[key] = value
        else:
            raise AttributeError

    def __str__(self):
        ans = []
        for key in string.ascii_lowercase:
            if hasattr(self, key):
                ans.append(f'{key}: {getattr(self, key)}')
        return ', '.join(ans)


# print('ab' in list(string.ascii_lowercase))
# try:
#     alp0 = Alpha(fistailo=10, raka=2, maka=42, fo=10)
# except AttributeError:
#     print(':(')
# alp = Alpha(c=10, z=2, a=42)
# try:
#     alp.ab = 123
# except AttributeError:
#     print(':(')
# alp.e = 123
# print(alp)
#
# try:
#     alp0 = AlphaQ(fistailo=10, raka=2, maka=42, fo=10)
# except AttributeError:
#     print(':(')
# alq = AlphaQ(c=10, z=2, a=42)
# try:
#     alp.ab = 123
# except AttributeError:
#     print(':(')
# alq.e = 123
# print(alq)

exec(sys.stdin.read())
