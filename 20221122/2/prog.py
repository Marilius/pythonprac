import sys

text = sys.stdin.buffer.read()
print(text.decode('UTF-8', errors='replace').encode('latin1', errors='replace').decode('CP1251', errors='replace'))
