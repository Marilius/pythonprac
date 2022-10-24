from collections import Counter
w = int(input())
data = []
curr = input()
while curr:
    for i in curr:
        if i.isalpha():
            data.append(i.lower())
        else:
            data.append(' ')
    curr = input()

f = lambda x: len(x) == w
data = list(Counter(list(filter(f, ''.join(data).split()))).items())
data.sort(key=lambda x: -x[1])
# print(data)
for i in data:
    if i[1] == data[0][1]:
        print(i[0], end=' ')
# print(data)
