import sys
from collections import UserString


class DivStr(UserString):
    def __init__(self, data=""):
        super().__init__(data)

    def __floordiv__(self, other):
        n = len(self) // other
        return iter(self[i:i + n] for i in range(0, other * n, n)) if n else iter('')

    def __mod__(self, other):
        n = len(self) % other
        return self[-n:]


# a = DivStr("XcDlaoalaofQWEasdssssERTdfgRTY")
# print(*a // 5)
# print(a % 5)
# print(*a % 43 // 14)
# print(a.lower() % 3)
# print(*a[1:7] // 3)
# print(a % 5 + DivStr() + a % 6)
exec(sys.stdin.read())
