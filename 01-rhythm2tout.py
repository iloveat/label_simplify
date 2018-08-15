# -*- coding: utf-8 -*-

"""
将用户标注的韵律文件分成单个 tout 文件
"""


import os


work_path = os.getcwd()
tout_path = work_path + '/tout/'
if not os.path.exists(tout_path):
    os.mkdir(tout_path)


rhythm_file_name = 'rhythm.txt'

with open(rhythm_file_name, "rb") as f:
    file_names = f.readlines()
    idx = 0
    for s in file_names:
        # print s
        s = s.strip('\r\n') + '\n'
        if idx % 2 == 0:
            name = s.split('\t')[0]
            name = tout_path + name + '.tout'
            outfile = open(name, "w+")
            outfile.write(s)
        else:
            outfile.write(s)
            outfile.close()
        idx += 1











