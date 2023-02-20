import datetime 
import os

currentDate = datetime.date.today()

data = currentDate.strftime("%Y%m%d")
isExist = os.path.exists(data)

if not isExist:
    os.makedirs(data)
    print("The new directory is created!")

for i in range(0, 1):
    path = f'{data}/{i}'
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    open(f'{path}/prog.py', 'a+')
    path = f'{path}/tests'

    if not isExist:
        os.makedirs(path)

    for j in range(1, 4):
        open(f'{path}/{j}.in', 'a+')
        open(f'{path}/{j}.out', 'a+')
