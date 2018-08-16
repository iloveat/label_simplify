# -*- coding: utf-8 -*-

"""
将 tout 和 interval 文件生成 xwal，增加英文字母版
Intervals + tout -> Intervals
版本：python3.5
"""


import os
import re


letter = {'A': 1,
          'B': 2,
          'C': 2,
          'D': 2,
          'E': 1,
          'F': 2,
          'G': 2,
          'H': 2,
          'I': 1,
          'J': 2,
          'K': 2,
          'L': 2,
          'M': 2,
          'N': 2,
          'O': 1,
          'P': 2,
          'Q': 3,
          'R': 2,
          'S': 2,
          'T': 2,
          'U': 2,
          'V': 2,
          'W': 6,
          'X': 3,
          'Y': 2,
          'Z': 2}

work_path = os.getcwd()

# output path
xwal_path = work_path + '/xwal/'
if not os.path.exists(xwal_path):
    os.mkdir(xwal_path)

# input path
tout_path = work_path + '/tout/'
interval_path = work_path + '/Intervals/'
interval_name_list = os.listdir(interval_path)


for file_name in interval_name_list:  # 遍历interval目录
  print(file_name)
  tout_name = re.sub(r'interval$', 'tout', file_name)
  xwal_name = re.sub(r'interval$', 'xwal', file_name)
  interval_file = open(interval_path + file_name, 'r')
  tout_file = open(tout_path + tout_name, 'r')
  xwal_file = open(xwal_path + xwal_name, 'w+')

  """
  ************以下生成xwal文件*******************
  """
  line1 = 'FileName:' + xwal_name
  interval_value_list = interval_file.read().split('\n')  # 把文件按换行符转成列表
  interval_file.close()
  line2 = 'time:' + interval_value_list[10]  # 获取文件时长
  line3 = '1.时间2.声母3.韵母4.音节5.中文6.声调7.重读8.儿化音9.韵律词10.韵律短语11.语调短语12.句子'
  line4 = '%10d\t\t2\t\t3\t\t4\t 5\t 6\t 7\t 8\t 9\t10\t11\t  12' % 1

  # 读取tout文件内容
  tout_value_list = tout_file.read().split('\n')
  tout_file.close()
  tout_rhythm = tout_value_list[0]

  # 先获取tout中的英文字母信息
  letter_list = []  # 本句话的英文字母
  for i in range(len(tout_rhythm)):
    if(re.search('[a-zA-Z]', tout_rhythm[i])):
      if(re.search('[a-z]', tout_rhythm[i])):  # 若是小写，转大写
        letter_list.append(tout_rhythm[i].upper())
      else:
        letter_list.append(tout_rhythm[i])

  # 检查tout文件标注是否缺失
  tout_pure_text = re.sub(r'#\d', '', tout_rhythm.split('\t')[1])  # 去掉韵律的纯文本
  print(tout_pure_text)
  tout_pinyin_list = tout_value_list[1].split('/')  # 注音的list
  print(tout_pinyin_list)

  sheng_mu = []  # 声母
  yun_mu = []  # 韵母
  tone = []  # 声调
  endtime = []  # 结束时间
  er_hua = []  # 儿化音
  line_index = 0

  interval_value_list = interval_value_list[12:]  # 从13行开始截取，音素的开始和结束时间
  for line in interval_value_list:
    line_index += 1
    if(re.search(r'"$', line)):  # 先匹配“结尾
      if(re.search(r'sil|sp', line)):   # 匹配是否是sil或sp
        endtime.append(int(float(interval_value_list[line_index-2])*(10**7)))  # 保留10^7次纳秒，htk以100ns为单位
        if(re.search(r'sil', line)):
          sheng_mu.append('sil')
          yun_mu.append('nil')
        else:
          sheng_mu.append('sp')
          yun_mu.append('nil')
        tone.append('x')
        er_hua.append('x')
        tout_pinyin_list.insert(len(er_hua)-1, ' ')
        num = line_index
      elif (re.search(r'ar|air|angr|aor|engr|iaor|iar|ingr|iour|ir|inr|our|uar|uair|uangr|ueir|uor|ur|vanr|vr|ver|vnr|eir|ier|iongr|uanr|anr|enr|or|ueir|ongr', line) or
              (re.search(r'er', line) and re.search(r'\wer\d', tout_pinyin_list[len(er_hua)-1]) and len(er_hua) == 1) or
              (re.search(r'er', line) and re.search(r'\wer\d', tout_pinyin_list[len(er_hua)]))):  # 儿化音
        endtime.append(int(float(interval_value_list[line_index-2])*(10**7)))
        if(line_index-num==3):
          sheng_mu.append('zero')
        yun_mu.append(line[1:(len(line)-2)])
        tone.append(line[-2])
        er_hua.append('1')
        num = line_index
      elif(re.search(r'^"ENG', line)):  # 英文字母
        endtime.append(int(float(interval_value_list[line_index-2])*(10**7)))
        sheng_mu.append('zero')
        yun_mu.append(line[1:-2])
        tone.append('7')
        er_hua.append('0')
        num = line_index
      elif(re.search(r'\d"$', line)):
        endtime.append(int(float(interval_value_list[line_index-2])*(10**7)))
        er_hua.append('0')
        if(re.search(r'iy', line)):  # iy->iii, zhi chi shi ri
          yun_mu.append('iii')
        elif(re.search(r'ix',line)):
          yun_mu.append('ii')  # ix->ii, zi ci si
        elif(re.search(r'\d\d"$', line)):  #双声位
          yun_mu.append(line[1:(len(line)-3)])
        else:
          yun_mu.append(line[1:(len(line)-2)])
        if(int(line[-2])==6):  # 上声变调，按2声处理
          tone.append('2')
        else:
          tone.append(line[-2])  # 双声位的只保留轻声5
        if(line_index-num==3):
          sheng_mu.append('zero')
        num = line_index
      else:
        sheng_mu.append(line[1:(len(line)-1)])

  hanzi=[]            #汉字
  syllable=[]         #音节
  stress=[]           #重音
  #er_hua=[]            #儿化音
  pWord=[]            #韵律词
  pPhrase=[]          #韵律短语
  iPhrase=[]          #语调短语
  sen=[]              #句子
  #toutString=tout_file.read()
  #toutlist=toutString.split('\n')
  #print(toutlist[0])
  #tout1=toutlist[0]
  #tout2=toutlist[1]
  tout1=tout_rhythm
  tout2=tout_value_list[1]
  tout1=tout1[8:]                 #从第一行的第8个字开始分析
  tout2=tout2[1:-1]               #去掉第二行开头的\t和结尾的'/'

  tout2=tout2.split('/')        #按空格切分
  num=0
  syllable.append('sil')           #句子开头sil
  #er_hua.append(' ')
  print(sheng_mu,'\n',yun_mu,'\n',er_hua,'\n',tone,'\n')
  #print(sheng_mu)
  #print(er_hua)
  lab = 0
  for index in range(len(tout2)):
    num+=1
    word=tout2[index]
    temp=word.split()             #去空格
    word=''.join(temp)
    #print(word)
    if(re.search(r'^E',word) ):          #字母
      #print(word)
      if(lab == 1):
        #print("**********")
        #print(num)
        num -= 1
        continue
      lab = 1

      while('ENG' in yun_mu[num] or ( sheng_mu[num]=='sp' and 'ENG' in yun_mu[num+1])):
        #print(num)
        #print(word)
        if('ENG' in yun_mu[num]):
          syllable.append(yun_mu[num])
          #if(sheng_mu[num+1] != 'ENG'):
            #num+=1
            #print("@@@@@@@@@@@@@")
            #break
        else:
          syllable.append('sp')
          syllable.append(yun_mu[num+1])
          num+=1
        #print(syllable)
        num+=1
      num -= 1
      #print(num)
      continue
    else:
      word=word[:len(word)-1]
      tone_tout=tout2[index][-1]        #取tout中的声调

    #print(word)
    #print(num)
    #print(sheng_mu[num])
    lab = 0
    if(er_hua[num]=='1'):                  #儿化音
      if(tone_tout == '5'):
        syllable.append(word[:len(word)-1])
        print(word,syllable)
      else:
        syllable.append(word)
        print(word,syllable)
    #  er_hua.append('1')             #儿化音标记1，其余标空
    elif(sheng_mu[num]=='sp'):
      syllable.append('sp')
      #word=tout2[index+1]
      #word=word[:len(word)-1]
      #print(num)
      #if(sheng_mu[num+1]!='ENG'):

      syllable.append(word)
      #print(syllable)
    #  er_hua.append(' ')
    #  er_hua.append(' ')
      num+=1
    elif(re.search(r'\d',word)):    #双声位

      word=word[:len(word)-1]
      syllable.append(word)
    else:
      syllable.append(word)
      #print(word)
    #  er_hua.append(' ')
  syllable.append('sil')            #句子尾部
  #er_hua.append(' ')

  #print(syllable)
#**********边界标记************
  hanzi.append('。')
  pWord.append(' ')
  pPhrase.append(' ')
  iPhrase.append(' ')
  sen.append(' ')
  stress.append(' ')
  num=0
  label=0
  lastnum = 0
  for s in tout1:
    boundary=s
    if(num>lastnum):
      label = 0
    if(re.search(r'[#，、。！‘’“”？《》·——：；()]',boundary)):  #tout中的特殊标点做判断
      continue
    elif(boundary=='1'):              #韵律词边界
      pWord[-1]='pw'
    elif(boundary=='2'):             #韵律短语边界
      pWord[-1]='pw'
      pPhrase[-1]='pp'
    elif(boundary=='3'):            #语调短语边界
      pWord[-1]='pw'
      pPhrase[-1]='pp'
      iPhrase[-1]='ip'
    elif(boundary=='4'):             #句子边界
      pWord[-1]='pw'
      pPhrase[-1]='pp'
      iPhrase[-1]='ip'
      sen[-1]='sen'
    elif(er_hua[num]=='1' and label==0):
      #print(num,hanzi[-1])
      hanzi[-1]=hanzi[-1]+s
      label=1
      lastnum = num
      #print(num)
      #num+=1
    else:
      num+=1
      #print(num,s,syllable[num])
      #print(num,s,len(syllable))
      if(syllable[num]=='sp' ):         #注意逗号是中文下的   #and (not re.search(r'，',s))
        #print(num,s)
        num+=1
        hanzi.append('，')             #中文输入法的逗号
        hanzi.append(s)
        pWord.append(' ')
        pWord.append(' ')
        pPhrase.append(' ')
        pPhrase.append(' ')
        iPhrase.append(' ')
        iPhrase.append(' ')
        sen.append(' ')
        sen.append(' ')
        stress.append(' ')
        stress.append(' ')
      else:
        hanzi.append(s)
        pWord.append(' ')
        pPhrase.append(' ')
        iPhrase.append(' ')
        sen.append(' ')
        stress.append(' ')
  pWord.append(' ')
  pPhrase.append(' ')
  iPhrase.append(' ')
  sen.append(' ')
  stress.append(' ')
  hanzi.append('。')
  #print(hanzi)
  #写文件
  xwal_file.write(line1+'\n'+line2+'\n'+line3+'\n'+line4+'\n')
  #print(len(endtime),len(er_hua),len(pWord),len(pPhrase),len(sen),len(stress),len(hanzi))

  for i in range(len(endtime)):
    outxwal=('%10s'+';\t'+'%5s'+';\t'+'%5s'+';\t'+'%5s'+';\t'+'%2s'+';\t'+'%2s'+';\t'+'%2s'+';\t'+'%2s'+ \
      ';\t'+'%2s'+';\t'+'%2s'+';\t'+'%2s'+';\t'+'%4s'+';'+'\n')%(str(endtime[i]),sheng_mu[i],yun_mu[i],syllable[i], \
      hanzi[i],tone[i],stress[i],er_hua[i],pWord[i],pPhrase[i],iPhrase[i],sen[i])
    xwal_file.write(outxwal)



  xwal_file.close()

