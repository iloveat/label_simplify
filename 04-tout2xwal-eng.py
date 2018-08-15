# -*- coding: utf-8 -*-
# author:sqb, hdl

"""
将 tout 和 interval 文件生成 xwal，增加英文字母版
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
intervalpath = work_path + '/Intervals/'

newintervalpath = work_path + '/interval1/'
if not os.path.exists(newintervalpath):
  os.mkdir(newintervalpath)

errorintervalpath = work_path + '/interval2/'
if not os.path.exists(errorintervalpath):
  os.mkdir(errorintervalpath)

toutpath = work_path + '/tout/'
xwalpath = work_path + '/xwal/'
if not os.path.exists(xwalpath):
  os.mkdir(xwalpath)


###排查错误阶段，需要打开此步骤

# intervallist=os.listdir(intervalpath)
# for intervalfile in intervallist:                   #遍历interval目录
#   print(intervalfile)
#   shutil.move(intervalpath+intervalfile,errorintervalpath+intervalfile) #移动错误文件到新目录
#   break


intervallist=os.listdir(intervalpath)
for intervalfile in intervallist:                   #遍历interval目录
  print(intervalfile)
  toutfile=re.sub(r'interval$','tout',intervalfile)  #用tout替换interval
  intervalNewPath=intervalpath+intervalfile
  intervalFile=open(intervalNewPath,'r')            #打开interval文件
  toutNewPath=toutpath+toutfile
  toutFile=open(toutNewPath,'r')                    #打开tout文件
  xwalfile=re.sub(r'interval$','xwal',intervalfile)
  xwalNewPath=xwalpath+xwalfile
  xwalFile=open(xwalNewPath,'w+')                   #打开xwal文件
  '''
  ************以下生成xwal文件*******************
  '''
  endtime=[]                                    #结束时间
  initial=[]                                    #声母
  final=[]                                      #韵母
  tone=[]                                       #声调
  erhua=[]                                      #儿化音

  line1='FileName:'+xwalfile
  line3='1.时间2.声母3.韵母4.音节5.中文6.声调7.重读8.儿化音9.韵律词10.韵律短语11.语调短语12.句子'
  line4=('%10s\t\t2\t\t3\t\t4\t  5\t\t6\t7\t8\t9\t10\t11\t  12')%(1)
  intervalString=intervalFile.read()
  intervallist=intervalString.split('\n')       #把文件按换行符转成列表
  line2='time:'+intervallist[10]                        #获取文件时长
  intervallist=intervallist[12:]                #从13行开始截取列表
  linenum=0
  letter_phone=''        #当前字母的音素
  letter_phone_num=0
  letter_value=0

  #先获取tout英文字母信息
  letter_cur=[]                                 #本句话的英文字母
  letter_num=0
  tout_temp = toutFile.read()
  tout_temp2 = tout_temp.split('\n')
  tout_temp3 = tout_temp2[0]
  
  for i in range(len(tout_temp3)):
    if(re.search('[a-zA-Z]',tout_temp3[i])):
      #print(tout_temp3[i])
      if(re.search('[a-z]',tout_temp3[i])):         #若是小写，转大写
        upletter=tout_temp3[i]
        templetter=upletter.upper()
        letter_cur.append(templetter)
      else:
        letter_cur.append(tout_temp3[i])
      letter_num += 1
      
  #检查tout文件标注是否缺失
  tout_temp4 = tout_temp3.split('\t')
  tout_temp5 = re.sub(r'#\d','',tout_temp4[1])              #去掉韵律的纯文本
  print(tout_temp5)
  tout_temp6 = tout_temp2[1].split('/')             #注音的list
  print(tout_temp6)
  '''
  for w in range(len(tout_temp5)):
    if not (re.match(r'\w',tout_temp5[w])):
        tout_temp6.insert(w,' ')
  '''



  for line in intervallist:                     #取interval文件信息
    linenum+=1

    if(re.search(r'"$',line)):                  #先匹配“结尾
      if(re.search(r'sil|sp',line)):            #匹配是否是sil或sp
        endtime.append(int(float(intervallist[linenum-2])*(10**7))) #保留10^7次纳秒，htk以100ns为单位
        
        if(re.search(r'sil',line)):
          initial.append('sil')
          final.append('nil')
        else:
          initial.append('sp')
          final.append('nil')
        tone.append('x')
        erhua.append('x')
        tout_temp6.insert(len(erhua)-1,' ')
        num=linenum
      #elif(re.search(r'rr"$',line) or re.search(r'er"$',line)):              #儿化音
      
      elif(re.search(r'ar|air|angr|aor|engr|iaor|iar|ingr|iour|ir|inr|our|uar|uair|uangr|ueir|uor|ur|vanr|vr|ver|vnr|eir|ier|iongr|uanr|anr|enr|or|ueir|ongr',line) or
           (re.search(r'er',line) and re.search(r'\wer\d',tout_temp6[len(erhua)])) or
           (re.search(r'er', line) and re.search(r'\wer\d', tout_temp6[len(erhua)-1]) and len(erhua)==1)):              #儿化音
        #print(line)
        #endtime[-1]=int(float(intervallist[linenum-2])*(10**7))
        #final[-1]=final[-1]+'r'
        endtime.append(int(float(intervallist[linenum-2])*(10**7)))
        erhua.append('1')
        #erhua[-1]='1'
        tone.append(line[-2])
        if(linenum-num==3):
          initial.append('zero')
        #else:
          #initial.append(line[1:(len(line)-1)])
        final.append(line[1:(len(line)-2)])
        num=linenum
      elif(re.search(r'^"ENG',line)):         #英文字母

        letter_phone=letter_cur[letter_value]
        len_letter_cur = letter[letter_phone]   #音素长度
        letter_phone_num += 1

        if(letter_phone_num==1): # hdl
        # if(letter_phone_num==len_letter_cur):	# sqb

          endtime.append(int(float(intervallist[linenum-2])*(10**7)))
          erhua.append('0')
          initial.append('zero')
          final.append(line[1:-2])
          tone.append('7')
          num=linenum
          letter_phone_num = 0
          letter_value += 1

      elif(re.search(r'\d"$',line)):
        endtime.append(int(float(intervallist[linenum-2])*(10**7)))
        erhua.append('0')
        if(re.search(r'iy',line)):              #iy->iii    zhi  chi  shi  ri
          final.append('iii')
        elif(re.search(r'ix',line)):
          final.append('ii')                    #ix->ii     zi  ci   si
        elif(re.search(r'\d\d"$',line)):        #双声位
          final.append(line[1:(len(line)-3)])
        else:
          final.append(line[1:(len(line)-2)])

        if(int(line[-2])==6):                 #上声变调,按2声处理
          tone.append('2')
        else:
          tone.append(line[-2])               #双声位的只保留轻声5
        if(linenum-num==3):
          initial.append('zero')
        num=linenum
      else:
        initial.append(line[1:(len(line)-1)])

  hanzi=[]            #汉字
  syllable=[]         #音节
  stress=[]           #重音
  #erhua=[]            #儿化音
  pWord=[]            #韵律词
  pPhrase=[]          #韵律短语
  iPhrase=[]          #语调短语
  sen=[]              #句子
  #toutString=toutFile.read()
  #toutlist=toutString.split('\n')
  #print(toutlist[0])
  #tout1=toutlist[0]
  #tout2=toutlist[1]
  tout1=tout_temp3
  tout2=tout_temp2[1]
  tout1=tout1[8:]                 #从第一行的第8个字开始分析
  tout2=tout2[1:-1]               #去掉第二行开头的\t和结尾的'/'

  tout2=tout2.split('/')        #按空格切分
  num=0
  syllable.append('sil')           #句子开头sil
  #erhua.append(' ')
  print(initial,'\n',final,'\n',erhua,'\n',tone,'\n')
  #print(initial)
  #print(erhua)
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

      while('ENG' in final[num] or ( initial[num]=='sp' and 'ENG' in final[num+1])):
        #print(num)
        #print(word)
        if('ENG' in final[num]):
          syllable.append(final[num])
          #if(initial[num+1] != 'ENG'):
            #num+=1
            #print("@@@@@@@@@@@@@")
            #break
        else:
          syllable.append('sp')
          syllable.append(final[num+1])
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
    #print(initial[num])
    lab = 0
    if(erhua[num]=='1'):                  #儿化音
      if(tone_tout == '5'):
        syllable.append(word[:len(word)-1])
        print(word,syllable)
      else:
        syllable.append(word)
        print(word,syllable)
    #  erhua.append('1')             #儿化音标记1，其余标空
    elif(initial[num]=='sp'):
      syllable.append('sp')
      #word=tout2[index+1]
      #word=word[:len(word)-1]
      #print(num)
      #if(initial[num+1]!='ENG'):

      syllable.append(word)
      #print(syllable)
    #  erhua.append(' ')
    #  erhua.append(' ')
      num+=1
    elif(re.search(r'\d',word)):    #双声位

      word=word[:len(word)-1]
      syllable.append(word)
    else:
      syllable.append(word)
      #print(word)
    #  erhua.append(' ')
  syllable.append('sil')            #句子尾部
  #erhua.append(' ')

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
    elif(erhua[num]=='1' and label==0):
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
  xwalFile.write(line1+'\n'+line2+'\n'+line3+'\n'+line4+'\n')
  #print(len(endtime),len(erhua),len(pWord),len(pPhrase),len(sen),len(stress),len(hanzi))

  for i in range(len(endtime)):
    outxwal=('%10s'+';\t'+'%5s'+';\t'+'%5s'+';\t'+'%5s'+';\t'+'%2s'+';\t'+'%2s'+';\t'+'%2s'+';\t'+'%2s'+ \
      ';\t'+'%2s'+';\t'+'%2s'+';\t'+'%2s'+';\t'+'%4s'+';'+'\n')%(str(endtime[i]),initial[i],final[i],syllable[i], \
      hanzi[i],tone[i],stress[i],erhua[i],pWord[i],pPhrase[i],iPhrase[i],sen[i])
    xwalFile.write(outxwal)

  intervalFile.close()                           #关闭文件
  toutFile.close()
  xwalFile.close()

  # shutil.move(intervalpath+intervalfile,newintervalpath+intervalfile) #移动正确文件到新目录
