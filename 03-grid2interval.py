# -*- coding: utf-8 -*-

"""
将格式从 TextGrid 转为 interval
interval_ex -> Intervals
版本：python3.5
"""


import os


work_path = os.getcwd()

# output path
output_path = work_path + '/Intervals/'
if not os.path.exists(output_path):
    os.mkdir(output_path)

# input path
input_path = work_path + '/interval_ex/'
file_name_list = os.listdir(input_path)

for file_name in file_name_list:
    print(file_name)

    input_file = open(input_path + file_name, 'r')
    input_txt = input_file.read()
    input_file.close()

    txt = input_txt.split(' ')
    txt = ''.join(txt).split('\n')

    total_time = txt[12].split('=')[1]
    total_phone = txt[13].split('=')[1]

    temp = input_txt.split('\n')
    out_file = open(output_path + file_name, 'w+')
    out_file.write(temp[0]+'\n'+temp[1]+'\n'+txt[2]+'\n'+'0'+'\n'+total_time+'\n'+'<exists>'+'\n'+'1'+'\n')
    out_file.write('"IntervalTier"'+'\n'+'"label"'+'\n'+'0'+'\n'+total_time+'\n'+total_phone+'\n')

    n = 0
    for i in range(len(txt)-1):
        if i < 14:
            continue
        else:
            if n == 0:
                n += 1
                continue
            else:
                n += 1
                if n == 4:
                    n = 0
                out_file.write(txt[i].split('=')[1]+'\n')

    out_file.close()



































