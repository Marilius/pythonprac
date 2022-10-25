print(*sorted(filter(lambda x: x.count('TOR') == 2, map(''.join, __import__('itertools').product("TOR", repeat=int(input()))))), sep=', ')
