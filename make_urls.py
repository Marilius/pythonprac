import os
curr_path = os.getcwd()
for file in os.listdir(curr_path):
    d = os.path.join(curr_path, file)
    if os.path.isdir(d):
        if len(d.split('\\')[-1]) > 5:
            for sub_d in os.listdir(d):
                sub_d_name = f'{d}\\{sub_d}'
                urls_curr_path = f'{sub_d_name}\\URLS'
                print(urls_curr_path)
                date, task_num = urls_curr_path.split('\\')[-3:-1]
                print(date, task_num)

                s1 = f'https://git.cs.msu.ru/s02200541/prak_repo/-/tree/main/{date}/{task_num}/tests\n'
                s2 = f'https://git.cs.msu.ru/s02200519/pythonprac/-/blob/master/{date}/{task_num}/tests\n'
                s3 = f'https://git.cs.msu.ru/s02200328/pythonprac/-/blob/main/{date}/{task_num}/tests\n'

                with open(urls_curr_path, 'w') as f:
                    f.write(s1)
                    f.write(s2)
                    f.write(s3)

                '''
                https://git.cs.msu.ru/s02200541/prak_repo/-/tree/main/ - lesha
                https://git.cs.msu.ru/s02200519/pythonprac/-/blob/master/ - andrey
                https://git.cs.msu.ru/s02200328/pythonprac/-/blob/main/ - nikita
                '''
