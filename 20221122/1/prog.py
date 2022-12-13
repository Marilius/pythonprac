import sys

text = sys.stdin.buffer.read()
# print(text)

n, text = text[0], text[1:]
l = len(text) - 1
ans = []

for i in range(n):
    curr = text[round(i*l/n):round((i+1)*l/n)]
    if curr:
        ans.append(curr)
sys.stdout.buffer.write(bytes([n]) + b''.join(sorted(ans)))
