import re
from pwn import *

s='/challenge/run'
p=process(s)
lvs=[b' UC ',b' C ',b' S ',b' TS ']
#       1       2      3      4
action=[b' read',b' write']
cat=[b'NUC',b'NATO',b'ACE',b'UFO']
#       1       2      3      4
sub_cat=[]
obj_cat=[]
#главный цикл
for i in range(21):
    print(i,'\n')
    sub_cat.clear()
    obj_cat.clear()
    tmp=p.recvuntil(b'Q ')
    qwe=p.recvline()
    #print (qwe)
    x=0
    read=qwe.find(action[0])
    # READ==TRUE, if action=read!!!
    if (read>0): act=0
    else: act=1
    print('act=',act,'\n')
# в переменной act хранится действие        
    for x in range(3):
        sub_l=qwe.find(lvs[x])
        if (sub_l>0 and sub_l<50): 
               subject_level=x+1
        obj_l=qwe.rfind(lvs[x])
        if (obj_l>50): 
               object_level=x+1
#получили уровни субъекта sub_l и объекта obj_l    
    y=0
    for y in range(4):
        sub_cat_pos=qwe.find(cat[y])
        if (sub_cat_pos>0) and (sub_cat_pos<80):
            sub_cat.append(y+1)
#получили массив из категорий субъекта
    y=0
    for y in range(4):
        obj_cat_pos=qwe.rfind(cat[y])
        if obj_cat_pos>80: obj_cat.append(y+1)
        #получили массив из категорий объекта
    if_read=set(sub_cat)>=set(obj_cat)
    if_write=set(obj_cat)>=set(sub_cat)
    if act==0:
        if subject_level>=object_level and if_read: 
           p.sendline(b'yes')
        else: 
           p.sendline(b'no')
    if (act==1):
        if object_level>=subject_level and if_write:
           p.sendline(b'yes')
        else: p.sendline(b'no')
#=====================================
p.close()
