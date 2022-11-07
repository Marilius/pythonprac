class morse:
    def __init__(self, value=''):
        self.ans = ''
        self.d = {'+': 'di', '.': 'dit', '-': 'dah'}
        self.end = ''
        value1 = value.split()
        if len(value1) == 1:
            pass
        elif len(value1) < 4:
            self.end = value[-1]
        elif len(value) == 4:
            self.end = value[3]




    def __pos__(self):
        self.ans += 'dit'
        return self

    def __neg__(self):
        self.ans += 'dah'
        return self

    def __str__(self):
        return self.ans




print(-+morse())
print(-++~+-+morse())
print(--+~-~-++~+++-morse())
print(--+~-~-++~+++-morse(".-"))
print(--+~-~-++~+++-morse("..-"))
print(--+~-~-++~+++-morse("..-|"))
print(--+~-~-++~+++-morse("dot DOT dash"))
print(--+~-~-++~+++-morse("ai aui oi "))
print(--+~-~-++~+++-morse("dot dot dash ///"))