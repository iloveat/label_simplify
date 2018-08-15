# -*- coding: utf-8 -*-

"""
将后缀 .TextGrid 转为 .interval
TextGrids -> interval_ex
版本：python3.5
"""


import os
import re


work_path = os.getcwd()

# output path
interval_path = work_path + '/interval_ex/'
if not os.path.exists(interval_path):
    os.mkdir(interval_path)

# input path
text_grid_path = work_path + '/TextGrids/'
file_name_list = os.listdir(text_grid_path)

for file_name in file_name_list:
    text_grid_name = text_grid_path + file_name
    text_grid_file = open(text_grid_name, 'r')
    text = text_grid_file.read()
    text_grid_file.close()

    interval_name = interval_path + re.sub(r'TextGrid$', 'interval', file_name)
    interval_file = open(interval_name, 'w+')
    interval_file.write(text)
    interval_file.close()





































