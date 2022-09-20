n = eval(input())

print(f'A {"+" if n % 25 == 0 and n % 2 == 0 else "-"}', end=' ')
print(f'B {"+" if n % 25 == 0 and n % 2 != 0 else "-"}', end=' ')
print(f'C {"+" if n % 8 == 0 else "-"}', end=' ')
