import re
from pwn import *
from sys import argv

s='/challenge/run'
p=process(s)
lvs=[]
action=[b' read',b' write']
cat=[]
sub_cat=[]
obj_cat=[]
#flag of the ending
flag_end=argv[1].encode()
#-----preparing-----------
p.recvuntil(b'40 Levels')
p.recvline()
for id in range(40):
    lvs.append(p.recvline().decode().strip())
lvs.reverse()
p.recvline()
for id in range(5):
    cat.append(p.recvline().decode().strip())

#главный цикл
for i in range(int(argv[1])):
    sub_cat.clear()
    obj_cat.clear()
    tmp=p.recvuntil(b'Q ')
    qwe=p.recvline()
    x=0
    read=qwe.find(action[0])
    if_flag=qwe.find(flag_end)
#READ==TRUE, if action=read!!!
    if (read>0): act=0
    else: act=1
#в переменной act хранится действие        
    for x in range(40):
        sub_l=qwe.find(lvs[x].encode())
        if (sub_l>0 and sub_l<50): 
               subject_level=x+1
        obj_l=qwe.rfind(lvs[x].encode())
        if (obj_l>50): 
               object_level=x+1
#получили уровни субъекта sub_l и объекта obj_l    
    y=0
    for y in range(5):
        sub_cat_pos=qwe.find(cat[y].encode())
        if (sub_cat_pos>0) and (sub_cat_pos<80):
            sub_cat.append(y+1)
#получили массив из категорий субъекта
    y=0
    for y in range(5):
        obj_cat_pos=qwe.rfind(cat[y].encode())
        if obj_cat_pos>80: obj_cat.append(y+1)
#получили массив из категорий объекта
    if_read=set(sub_cat)>=set(obj_cat)
    if_write=set(obj_cat)>=set(sub_cat)
    if act==0:
        if subject_level>=object_level and if_read: 
           string_to_send=b'yes'
        else: 
           string_to_send=b'no'
    if (act==1):
        if object_level>=subject_level and if_write:
           string_to_send=b'yes'
        else: string_to_send=b'no'
    if if_flag>=0: 
       p.sendline(string_to_send)
       p.recvuntil(b'pwn')
       flag=b'pwn'+p.recvuntil(b'}')
    else: p.sendline(string_to_send)
#=====================================
print('flag = ',flag.decode())
p.close()
