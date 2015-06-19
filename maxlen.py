# -*- encoding: cp1251 -*-

import time
import datetime
import os
import codecs

maxlen = [0]*21

class pm:
    def __init__(self):
        self.dt1 = datetime.datetime.now()
        self.dt2 = self.dt1

    def __str__(self):
        if self.dt1 == self.dt2:
            self.dt2 = datetime.datetime.now()
        return str(self.delta())

    def start(self):  
        self.dt1 = datetime.datetime.now()

    def stop(self):
        self.dt2 = datetime.datetime.now()
        return self
        
    def delta(self):
        return self.dt2 - self.dt1


def processline(ln):
    lst = ln.split('|');
    #print lst

    #for s in lst[1:-1]:
    #namelen = map(lambda x: len(x), [lst[2],lst[4],lst[6]])
    #namelen = map(lambda x: len(x), lst[2:7:2])
    #namelen = map(lambda x: len(x), lst[1:-1])

    if len(lst[17])>5:
        lst[16]=''

    if len(lst[21])>9:
        lst[21]=''

    if len(lst[19])>5:
        lst[19]=''

    if len(lst[17])>5:
        lst[17]=''

    if len(lst[15])>5:
        lst[15]=''

    if len(lst[9])>3:
        lst[9]=''

    if len(lst[8])>10:
        lst[8]=''
        
    namelen = [len(x) for x in lst[1:-1]]
    for i in range(21):
       if maxlen[i] < namelen[i]:
          maxlen[i] = namelen[i]

    if namelen[20] > 10 or namelen[18] >5 \
    or namelen[16] >5  or namelen[15] >5  or namelen[14] >5 \
    or namelen[8] >3 or namelen[7] >10:
        print '; '.join(lst[1:-1])

    #for x, mx in zip(namelen, maxlen):
    #   if x < mx:
    #      mx = x  
    #print namelen
    

def listfile(filename):
    z = pm()
    #fin = open(filename, 'r')
    fin = codecs.open(filename, 'r', encoding='cp1251')
    #print fin.encoding
    
    cnt = 0
    next(fin)
    for ln in fin:
        processline(ln)
        cnt = cnt + 1
        #if cnt==10:
        #   break

    fin.close()
    print(z)
    print filename, cnt
    print maxlen


def listfiles(path = '.'):
    z = pm()
    lst = [f for f in os.listdir(path) if f.endswith(".txt")]
    #print (lst)
    for f in lst:
        listfile(f)
        #break
    
    print("total:")    
    print(z)
    

listfiles()
print maxlen

#listfile(u"01.txt")



