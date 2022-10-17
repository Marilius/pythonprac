head = input()

h = len(head)
w = 1
data = []


gas = 0
liquid = 0

s = ''
while s != head:
    s = input()
    w += 1
    if s == head:
        break
    if s[1] == '.':
        gas += 1
    else:
        liquid += 1


gas_vol = gas * (h - 2)
liquid_vol = liquid * (h - 2)

liquid = liquid_vol // (w - 2)
if liquid_vol % (w - 2):
    liquid += 1
gas = h - liquid - 2

print('#' * w)
for i in range(h - 2):
    if gas != 0:
        print('#' + '.' * (w - 2) + '#')
        gas -= 1
    else:
        print('#' + '~' * (w - 2) + '#')
        liquid -= 1
print('#' * w)

digits = max(len(str(gas_vol)), len(str(liquid_vol)))


liquid_str = '~' * 20
gas_str = '.' * 20

if liquid_vol > gas_vol:
    gas_str = '.' * round(20 * gas_vol / liquid_vol) + ' ' * (20 - round(20 * gas_vol / liquid_vol))
elif gas_vol > liquid_vol:
    liquid_str = '~' * round(20 * liquid_vol / gas_vol) + ' ' * (20 - round(20 * liquid_vol / gas_vol))


print(gas_str, f'{gas_vol}/{gas_vol + liquid_vol}')
print(liquid_str, f'{liquid_vol}/{gas_vol + liquid_vol}')