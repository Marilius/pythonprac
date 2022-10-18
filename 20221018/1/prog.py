s = input().lower()
ans = set()
for i in range(1, len(s)):
    if s[i-1:i+1].isalpha():
        ans.add(s[i-1:i+1])
print(len(ans))
