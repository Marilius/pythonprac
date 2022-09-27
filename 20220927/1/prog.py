m, n = eval(input())
print([i for i in range(max(2, m), n) if all([i % j != 0 for j in range(2, i)])])