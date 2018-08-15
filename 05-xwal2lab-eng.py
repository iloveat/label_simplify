#!/usr/bin/env python
#filename:xwal2lab.py
#coding:utf-8
#autor:sqb, hdl
#time:2017-10-30
#本程序把xwal格式文件转成lab

import re , os , shutil

curpath=os.getcwd()
xwalpath=curpath+'/xwal/'

lab=os.path.exists('label')
if(not lab):
  os.mkdir('label')
  os.mkdir('label/old')
  os.mkdir('label/new-01')
labpath=r'./label/old/'
#xwallist=os.listdir(xwalpath)
sym=('0','1','2','3','4','5','6','7','8','9','10','11','12')
sym=('-','+','#','&','!','$','_','/',':','^','=','|','@')        #匹配符
#**********声母发音方式**********
affricate=('z','zh','j')        #塞擦音
asprt_affricate=('c','ch','q')        #塞擦送气
asprt_stop=('p','t','k')              #塞送气
fricative=('f','s','sh','r','x','h')    #擦音
lateral=('l')       #边音
nasal=('m','n')         #鼻音
#nil=('nil')         #静音段
stop=('b','d','g')
#zero=('zero')
method=(affricate,asprt_affricate,asprt_stop,fricative,lateral,nasal,stop)
#*********声母发音位置*****************
dentalveolar=('d','t','z','c','s','n','l')
dorsal=('j','q','x')
labial=('b','p','m')
labiodental=('f')
#nil=('nil')
retroflex=('zh','ch','sh','r')
velar=('g','k','h')
#zero=('zero')
place=()
#*********韵母的韵头发音方式**********
#nil=('nil')
front_open=('a','ai','an','ang','ao','o','ong','ou','e','ei','en','eng','er','ii','iii')
front_protruded=('v','van','ve','vn')
front_round=('u','ua','uai','uan','uang','uei','uen','ueng','uo')
front_strectched=('i','ia','ian','iang','iao','ie','in','ing','io','iong','iou')
#nasal  鼻音  一般没有
#**********韵母的韵尾发音方式************
rear_nasal=('an','en','ian','in','uan','uen','van','vn','ang','eng','iang','ing','iong','ong','uang','ueng')
#nil=('nil')
rear_open=('a','ao','e','ia','iao','ie','io','o','ua','uo','ve','ii','iii')
rear_protruded=('v')
rear_retroflex=('air','angr','aor','eir','engr','er','iaor','iar','ingr','iour','ir','our','uair','uangr','ueir','uor','ur' \
,'vanr','ver','vnr')
rear_round=('iou','ou','u')
rear_strectched=('ai','ei','i','uai','uei')
#******************************************
def methodfun(tmp):         #判断声母发音方法
  if(affricate[0]==tmp or affricate[1]==tmp or affricate[2]==tmp):
    ret=1
  elif(asprt_affricate[0]==tmp or asprt_affricate[1]==tmp or asprt_affricate[2]==tmp):
    ret=2
  elif(asprt_stop[0]==tmp or asprt_stop[1]==tmp or asprt_stop[2]==tmp):
    ret=3
  elif(fricative[0]==tmp or fricative[1]==tmp or fricative[2]==tmp or fricative[3]==tmp or fricative[4]==tmp or fricative[5]==tmp):
    ret=4
  elif(lateral[0]==tmp):
    ret=5
  elif(nasal[0]==tmp or nasal[1]==tmp):
    ret=6
  elif('sil'==tmp or 'sp'==tmp or 'nil'==tmp):
    ret=7
  elif(stop[0]==tmp or stop[1]==tmp or stop[2]==tmp):
    ret=8
  elif('zero'==tmp):
    ret=9
  else:
    ret=0
  return ret

def placefun(tmp):        #判断声母发音位置
  if(dentalveolar[0]==tmp or dentalveolar[1]==tmp or dentalveolar[2]==tmp or dentalveolar[3]==tmp or \
    dentalveolar[4]==tmp or dentalveolar[5]==tmp or dentalveolar[6]==tmp):
    ret=1
  elif(dorsal[0]==tmp or dorsal[1]==tmp or dorsal[2]==tmp):
    ret=2
  elif(labial[0]==tmp or labial[1]==tmp or labial[2]==tmp):
    ret=3
  elif(labiodental[0]==tmp):
    ret=4
  elif('nil'==tmp or 'sp'==tmp or 'sil'==tmp):
    ret=5
  elif(retroflex[0]==tmp or retroflex[1]==tmp or retroflex[2]==tmp or retroflex[3]==tmp):
    ret=6
  elif(velar[0]==tmp or velar[1]==tmp or velar[2]==tmp):
    ret=7
  elif('zero'==tmp):
    ret=8
  else:
    ret=0
  return ret

def frontFinal(tmp):                #韵母的韵头发音方式
  for i in range(len(front_open)):
    if(front_open[i]==tmp):
      ret=2
      return ret
  for i in range(len(front_protruded)):
    if(front_protruded[i]==tmp):
      ret=3
      return ret
  for i in range(len(front_round)):
    #print(front_round[i])
    if(front_round[i]==tmp):
      ret=4
      return ret
  for i in range(len(front_strectched)):
    if(front_strectched[i]==tmp):
      ret=5
      return ret
  if('nil'==tmp or 'sp'==tmp or 'sil'==tmp):
    ret=1
  else:
    ret=0
    #print(tmp)
  return ret

def rearFinal(tmp):
  for i in range(len(rear_nasal)):
    if(rear_nasal[i]==tmp):
      ret=1
      return ret
  for i in range(len(rear_open)):
    if(rear_open[i]==tmp):
      ret=3
      return ret
  for i in range(len(rear_protruded)):
    if(rear_protruded[i]==tmp):
      ret=4
      return ret
  for i in range(len(rear_retroflex)):
    if(rear_retroflex[i]==tmp):
      ret=5
      return ret
  for i in range(len(rear_round)):
    if(rear_round[i]==tmp):
      ret=6
      return ret
  for i in range(len(rear_strectched)):
    if(rear_strectched[i]==tmp):
      ret=7
      return ret
  if('nil'==tmp or 'sp'==tmp or 'sil'==tmp):
    ret=2
  else:
    ret=0
  return ret
#******************************************

xwallist=os.listdir(xwalpath)
for xwalone in xwallist:
  print(xwalone)
  xwalonepath=xwalpath+xwalone
  xwalfile=open(xwalonepath,'r')
  xwalString=xwalfile.read()
  xwalfile.close()
  labone=re.sub(r'xwal','lab',xwalone)
  labfilepath=labpath+labone
  labfile=open(labfilepath,'w+')
  xwallineList=xwalString.split('\n')         #以换行符切分
  xwallineList=xwallineList[4:-1]
  #新建列表，存各列信息
  time=[]
  initial=[]
  final=[]
  syllable=[]
  tone=[]
  erhua=[]
  pword=[]
  pphrase=[]
  iphrase=[]
  sen=[]
  lab=[]
  #读取文件信息
  for i in range(len(xwallineList)):          #循环处理每一行
    line=xwallineList[i]
    temp=line.split()                   #以空格切分，去掉字符串空格的方法
    line=''.join(temp)                  #''表示直接连接
    line=line.split(';')
    time.append(line[0])
    initial.append(line[1])
    final.append(line[2])
    syllable.append(line[3])
    tone.append(line[5])
    erhua.append(line[7])
    pword.append(line[8])
    pphrase.append(line[9])
    iphrase.append(line[10])
    sen.append(line[11])
  # '''
  # ******开始计算lab******
  # '''

  totalline=len(xwallineList)             #总的行数
  siltime=2000000                          #sil时间取200ms
  for i in range(totalline):                 #循环每一行

    if(i==0):                                #起止时间信息
      if(int(time[i]) > siltime ):
        starttime=str(int(time[i])-siltime)
      else:
        starttime = 0
    else:
      starttime=time[i-1]
    if(i==totalline-1):
      #print(time[totalline-1])
      if(int(time[totalline-1]) > int(time[totalline-2]) + siltime):
        endtime = str(int(time[totalline-2])+siltime)
      else:
        endtime = int(time[totalline-1])
    else:
      endtime=time[i]

    #****************A组***************    当前音节
    aa=[]
    aa.append(initial[i])
    aa.append(final[i])
    type=methodfun(initial[i])
    aa.append(str(type))
    type=placefun(initial[i])
    aa.append(str(type))
    type=frontFinal(final[i])
    aa.append(str(type))
    type=rearFinal(final[i])
    aa.append(str(type))
    aa.append(tone[i])

    #****************B组***************    前一音节
    bb=[]
    if(i==0):
      #bb=aa
      bb.append('sil')
      bb.append('nil')
      bb.append('7')
      bb.append('5')
      bb.append('1')
      bb.append('2')
      bb.append('0')
    else:
      bb.append(initial[i-1])
      bb.append(final[i-1])
      type=methodfun(initial[i-1])
      bb.append(str(type))
      type=placefun(initial[i-1])
      bb.append(str(type))
      type=frontFinal(final[i-1])
      bb.append(str(type))
      type=rearFinal(final[i-1])
      bb.append(str(type))
      bb.append(tone[i-1])

    #****************C组*****************      后一音节
    cc=[]
    if(i==totalline-1):
      #cc=aa
      cc.append('sil')
      cc.append('nil')
      cc.append('7')
      cc.append('5')
      cc.append('1')
      cc.append('2')
      cc.append('0')
    else:
      cc.append(initial[i+1])
      cc.append(final[i+1])
      type=methodfun(initial[i+1])
      cc.append(str(type))
      type=placefun(initial[i+1])
      cc.append(str(type))
      type=frontFinal(final[i+1])
      cc.append(str(type))
      type=rearFinal(final[i+1])
      cc.append(str(type))
      cc.append(tone[i+1])

    #***************D组*****************     正序位置
    if(initial[i]=='sil' or initial[i]=='sp'):        #sil和sp
      d1='0'
      d2=d3=d4=d5=d6=d7=d8=d9=d10=d1
    else:
      n=0
      for j in range(i-1,-1,-1):                   #syl_in_pw
        if(pword[j]=='pw'):
          d1=str(i-j-1-n)
          break
        elif(j==0):
          d1=str(i-1-n)
        elif((initial[j]=='sil' or initial[j]=='sp') and j!=0):
          n+=1
      n=0
      for j in range(i-1,-1,-1):                    #syl_in_pp
        if(pphrase[j]=='pp'):
          d2=str(i-j-1-n)
          break
        elif(j==0):
          d2=str(i-1-n)
        elif((initial[j]=='sil' or initial[j]=='sp') and j!=0):
          n+=1
      n=0
      for j in range(i-1,-1,-1):                    #syl_in_ip
        if(iphrase[j]=='ip'):
          d3=str(i-j-1-n)
          break
        elif(j==0):
          d3=str(i-1-n)
        elif((initial[j]=='sil' or initial[j]=='sp')and j!=0):
          n+=1
      n=0
      for j in range(i-1,-1,-1):                    #syl_in_sen
        if(sen[j]=='sen'):
          d4=str(i-j-1-n)
          break
        elif(j==0):
          d4=str(i-1-n)
        elif((initial[j]=='sil' or initial[j]=='sp')and j!=0):
          n+=1
      n=0
      for j in range(i-1,-1,-1):                   #pw_in_pp
        if(pphrase[j]=='pp'):
          d5=str(n)
          break
        elif(j==0):
          d5=str(n)
        if(pword[j]=='pw'):
          n+=1
      n=0
      for j in range(i-1,-1,-1):                   #pw_in_ip
        if(iphrase[j]=='ip'):
          d6=str(n)
          break
        elif(j==0):
          d6=str(n)
        if(pword[j]=='pw'):
          n+=1
      n=0
      for j in range(i-1,-1,-1):                   #pw_in_sen
        if(sen[j]=='sen'):
          d7=str(n)
          break
        elif(j==0):
          d7=str(n)
        if(pword[j]=='pw'):
          n+=1
      n=0
      for j in range(i-1,-1,-1):                   #pp_in_ip
        if(iphrase[j]=='ip'):
          d8=str(n)
          break
        elif(j==0):
          d8=str(n)
        if(pphrase[j]=='pp'):
          n+=1
      n=0
      for j in range(i-1,-1,-1):                   #pp_in_sen
        if(sen[j]=='sen'):
          d9=str(n)
          break
        elif(j==0):
          d9=str(n)
        if(pphrase[j]=='pp'):
          n+=1
      n=0
      for j in range(i-1,-1,-1):                   #ip_in_sen
        if(sen[j]=='sen'):
          d10=str(n)
          break
        elif(j==0):
          d10=str(n)
        if(iphrase[j]=='ip'):
          n+=1
  #****************E组******************             倒序位置
    if((initial[i]=='sil' or initial[i]=='sp')):        #sil和sp
      e1='0'
      e2=e3=e4=e5=e6=e7=e8=e9=e10=e1
    else:
      n=0
      for j in range(i,totalline):                   #syl_in_pw
        if(pword[j]=='pw'):
          e1=str(j-i-n)
          break
        elif((initial[j]=='sil' or initial[j]=='sp')):             #sp
          n+=1
      n=0
      for j in range(i,totalline):                    #syl_in_pp
        if(pphrase[j]=='pp'):
          e2=str(j-i-n)
          break
        elif((initial[j]=='sil' or initial[j]=='sp')):
          n+=1
      n=0
      for j in range(i,totalline):                    #syl_in_ip
        if(iphrase[j]=='ip'):
          e3=str(j-i-n)
          break
        elif((initial[j]=='sil' or initial[j]=='sp')):
          n+=1
      n=0
      for j in range(i,totalline):                    #syl_in_sen
        if(sen[j]=='sen'):
          e4=str(j-i-n)
          break
        elif((initial[j]=='sil' or initial[j]=='sp')):
          n+=1
      n=0
      for j in range(i,totalline):                   #pw_in_pp
        if(pphrase[j]=='pp'):
          e5=str(n)
          break
        elif(j==0):
          e5=str(n)
        if(pword[j]=='pw'):
          n+=1
      n=0
      for j in range(i,totalline):                   #pw_in_ip
        if(iphrase[j]=='ip'):
          e6=str(n)
          break
        elif(j==0):
          e6=str(n)
        if(pword[j]=='pw'):
          n+=1
      n=0
      for j in range(i,totalline):                   #pw_in_sen
        if(sen[j]=='sen'):
          e7=str(n)
          break
        elif(j==0):
          e7=str(n)
        if(pword[j]=='pw'):
          n+=1
      n=0
      for j in range(i,totalline):                   #pp_in_ip
        if(iphrase[j]=='ip'):
          e8=str(n)
          break
        elif(j==0):
          e8=str(n)
        if(pphrase[j]=='pp'):
          n+=1
      n=0
      for j in range(i,totalline):                   #pp_in_sen
        if(sen[j]=='sen'):
          e9=str(n)
          break
        elif(j==0):
          e9=str(n)
        if(pphrase[j]=='pp'):
          n+=1
      n=0
      for j in range(i,totalline):                   #ip_in_sen
        if(sen[j]=='sen'):
          e10=str(n)
          break
        elif(j==0):
          e10=str(n)
        if(iphrase[j]=='ip'):
          n+=1

    #*******************F组***************          #音节数目
    #print(e4,d4)
    if((initial[i]=='sil' or initial[i]=='sp')):        #sil和sp
      f1='0'
      f2=f3=f4=f5=f6=f7=f8=f9=f10=f1
    else:
      f1=str(int(e1)+int(d1)+1)
      f2=str(int(e2)+int(d2)+1)
      f3=str(int(e3)+int(d3)+1)
      f4=str(int(e4)+int(d4)+1)
      f5=str(int(e5)+int(d5)+1)
      f6=str(int(e6)+int(d6)+1)
      f7=str(int(e7)+int(d7)+1)
      f8=str(int(e8)+int(d8)+1)
      f9=str(int(e9)+int(d9)+1)
      f10=str(int(e10)+int(d10)+1)

    #print(i)
    #******************G组***************            #前一音节数目
    if((initial[i]=='sil' or initial[i]=='sp')):
      g1='0'
      g2=g3=g4=g5=g6=g7=g8=g9=g10=g1
    else:
      n=0
      label=0
      spnum=0
      for j in range(i-1,0,-1):
        if(pword[j]=='pw' and label==0):
          label=1
          n+=1
        elif(label==1):
          if(pword[j]=='pw'):
            break
          elif((initial[j]=='sil' or initial[j]=='sp')and j!=0):
            spnum+=1
            n+=1
          else:
            n+=1

      if(n-spnum==0):
        g1='0'
      else:
        g1=str(n-spnum)
      #print(n,spnum);
      n=0
      label=0
      spnum=0
      for j in range(i-1,0,-1):
        if(pphrase[j]=='pp' and label==0):
          label=1
          n+=1
        elif(label==1):
          if(pphrase[j]=='pp'):
            break
          elif((initial[j]=='sil' or initial[j]=='sp')and j!=0):
            spnum+=1
            n+=1
          else:
            n+=1

      if(n-spnum==0):
        g2='0'
      else:
        g2=str(n-spnum)

      n=0
      label=0
      spnum=0
      for j in range(i-1,0,-1):
        if(iphrase[j]=='ip' and label==0):
          label=1
          n+=1
        elif(label==1):
          if(iphrase[j]=='ip'):
            break
          elif((initial[j]=='sil' or initial[j]=='sp')and j!=0):
            spnum+=1
            n+=1
          else:
            n+=1

      if(n-spnum==0):
        g3='0'
      else:
        g3=str(n-spnum)

      n=0
      label=0
      for j in range(i-1,0,-1):
        if(pphrase[j]=='pp' and label==0):
          label=1
          n+=1
        elif(label==1):
          if(pphrase[j]=='pp'):
            break
          elif(pword[j]=='pw'):
            n+=1
      if(n==0):
        g4='0'
      else:
        g4=str(n)

      n=0
      label=0
      for j in range(i-1,0,-1):
        if(iphrase[j]=='ip' and label==0):
          label=1
          n+=1
        elif(label==1):
          if(iphrase[j]=='ip'):
            break
          elif(pword[j]=='pw'):
            n+=1
      if(n==0):
        g5='0'
      else:
        g5=str(n)

      n=0
      label=0
      for j in range(i-1,0,-1):
        if(iphrase[j]=='ip' and label==0):
          label=1
          n+=1
        elif(label==1):
          if(iphrase[j]=='ip'):
            break
          elif(pphrase[j]=='pp'):
            n+=1
      if(n==0):
        g6='0'
      else:
        g6=str(n)
    #****************H组******************         后一音节数目
    if((initial[i]=='sil' or initial[i]=='sp')):
      h1='0'
      h2=h3=h4=h5=h6=h7=h8=h9=h10=h1
    else:
      n=0
      label=0
      spnum=0
      for j in range(i,totalline):
        if(pword[j]=='pw' and label==0):
          label=1
        elif(label==1):
          if(pword[j]=='pw'):
            n+=1
            break
          elif((initial[j]=='sil' or initial[j]=='sp')and j!=totalline):
            spnum+=1
            n+=1
          else:
            n+=1

      if(n-spnum==0):
        h1='0'
      else:
        h1=str(n-spnum)
      #print(n,spnum);
      n=0
      label=0
      spnum=0
      for j in range(i,totalline):
        if(pphrase[j]=='pp' and label==0):
          label=1
        elif(label==1):
          if(pphrase[j]=='pp'):
            n+=1
            break
          elif((initial[j]=='sil' or initial[j]=='sp')and j!=totalline):
            spnum+=1
            n+=1
          else:
            n+=1

      if(n-spnum==0):
        h2='0'
      else:
        h2=str(n-spnum)
      #print(n,spnum)
      n=0
      label=0
      spnum=0
      for j in range(i,totalline):
        if(iphrase[j]=='ip' and label==0):
          label=1
        elif(label==1):
          if(iphrase[j]=='ip'):
            n+=1
            break
          elif((initial[j]=='sil' or initial[j]=='sp') and j!=totalline):
            spnum+=1
            n+=1
          else:
            n+=1
      if(n-spnum==0):
        h3='0'
      else:
        h3=str(n-spnum)
     # print(n,spnum,i,totalline)

      n=0
      label=0
      for j in range(i,totalline):
        if(pphrase[j]=='pp' and label==0):
          label=1
        elif(label==1):
          if(pphrase[j]=='pp'):
            n+=1
            break
          elif(pword[j]=='pw'):
            n+=1
      if(n==0):
        h4='0'
      else:
        h4=str(n)

      n=0
      label=0
      for j in range(i,totalline):
        if(iphrase[j]=='ip' and label==0):
          label=1
        elif(label==1):
          if(iphrase[j]=='ip'):
            n+=1
            break
          elif(pword[j]=='pw'):
            n+=1
      if(n==0):
        h5='0'
      else:
        h5=str(n)

      n=0
      label=0
      for j in range(i,totalline):
        if(iphrase[j]=='ip' and label==0):
          label=1
        elif(label==1):
          if(iphrase[j]=='ip'):
            n+=1
            break
          elif(pphrase[j]=='pp'):
            n+=1
      if(n==0):
        h6='0'
      else:
        h6=str(n)

#******************合成lab*********************

    aLab=sym[0]+aa[0]+sym[1]+aa[1]+sym[2]+aa[2]+sym[3]+aa[3]+sym[4]+aa[4]+sym[5]+aa[5]+sym[6]+aa[6]+sym[7]
    bLab=sym[8]+bb[0]+sym[0]+bb[1]+sym[2]+bb[2]+sym[4]+bb[3]+sym[6]+bb[4]+sym[9]+bb[5]+sym[12]+bb[6]+sym[7]
    cLab=sym[8]+cc[0]+sym[1]+cc[1]+sym[3]+cc[2]+sym[5]+cc[3]+sym[9]+cc[4]+sym[10]+cc[5]+sym[11]+cc[6]+sym[7]
    dLab=sym[8]+d1+sym[2]+d2+sym[5]+d3+sym[12]+d4+sym[10]+d5+sym[0]+d6+sym[3]+d7+sym[6]+d8+sym[12]+d9+sym[0]+d10+sym[7]
    eLab=sym[8]+e1+sym[3]+e2+sym[9]+e3+sym[11]+e4+sym[0]+e5+sym[4]+e6+sym[9]+e7+sym[1]+e8+sym[4]+e9+sym[2]+e10+sym[7]
    fLab=sym[8]+f1+sym[4]+f2+sym[3]+f3+sym[12]+f4+sym[1]+f5+sym[5]+f6+sym[10]+f7+sym[1]+f8+sym[6]+f9+sym[10]+f10+sym[7]
    gLab=sym[8]+g1+sym[5]+g2+sym[11]+g3+sym[1]+g4+sym[9]+g5+sym[4]+g6+sym[7]
    hLab=sym[8]+h1+sym[6]+h2+sym[11]+h3+sym[2]+h4+sym[6]+h5+sym[2]+h6+sym[7]
    Lab=('%10s'+' '+'%10s'+' '+aLab+'B'+bLab+'C'+cLab+'D'+dLab+'E'+eLab+'F'+fLab+'G'+gLab+'H'+hLab+'\n')%(starttime,endtime)
    labfile.write(Lab)
  labfile.close()
