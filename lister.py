# -*- encoding: cp1251 -*-
# cp1251 

import time
import datetime
import os
import codecs
import sys
#import MySQLdb as mdb

import mysql.connector

print "start"

conn  = mysql.connector.connect(user='root', password='root123',
                              host='127.0.0.1',
                              database='test',charset='cp1251')
#conn  = mdb.connect(host='127.0.0.1',user='root', passwd='root123',db='test',charset='cp1251',use_unicode=True)       

#conn  = mdb.connect(host='127.0.0.1',user='root', passwd='root123',db='test')       
#conn.set_character_set('cp1251')

c = conn.cursor()
c.execute("DROP TABLE IF EXISTS people;")
c.execute("CREATE TABLE people (id INT NOT NULL AUTO_INCREMENT, tax_number VARCHAR(10), name VARCHAR(50), surname VARCHAR(50), patronymic VARCHAR(50), rus_name_id INT, rus_surname_id INT, rus_patronymic_id INT, birthday DATE, country_id INT, area_id INT, region_id VARCHAR(5), locality_type VARCHAR(1), locality VARCHAR(80), street_type INT, street_id INT, building_number VARCHAR(5), building_letter VARCHAR(5), housing_number VARCHAR(5), appartment_number  VARCHAR(5), foring_locality_id BIGINT, old_id BIGINT, sex VARCHAR(1), PRIMARY KEY (id)) DEFAULT CHARACTER SET cp1251 COLLATE cp1251_bin;")
#                              1          2       3              4    5           6          7                 8        9          10      11        12            13       14          15        16              17              18             19                20                 21                  1    2   3   4   5   6   7   8   9  10  11  12    13 14 15 16   17   18   19   20 21
insstr = u"INSERT INTO people (tax_number,surname,rus_surname_id,name,rus_name_id,patronymic,rus_patronymic_id,birthday,country_id,area_id,region_id,locality_type,locality,street_type,street_id,building_number,building_letter,housing_number,appartment_number,foring_locality_id,old_id,sex) VALUE ('%s','%s',%d,'%s',%d,'%s',%d,'%s',%d,%d,'%s','%s','%s',%d,%d,'%s','%s','%s','%s',%d,%d,'%s');"

lsttoint = [3,5,7,9,10,11,14,15,20,21]

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


def toint(ll,z):
    if not ll[z].strip() or not ll[z].isdigit():
        ll[z] = 0
    else:
        ll[z] = int(ll[z])
    

def processline(ln):
    lst = ln.split('|');
    #print lst
    #instup = tuple(lst[1:-1])
    
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

    if len(lst[16])>5:
        lst[16]=''

    if len(lst[8])>10:
        lst[8]='00000000'

    if len(lst[8])==10:
        lst[8] = lst[8][6:10] + lst[8][3:5] + lst[8][0:2]
    else:
        lst[8] = '00000000'

    if int(lst[1][8])% 2 == 0:
        sex = u'Ж'
    else:
        sex = u'М'

    lst[22] = sex
    
    for x in lsttoint:
      toint(lst,x)    

    #        ('%s',   '%s',   %d,     '%s',   %d,     '%s',   %d,     '%s',   %d,     %d,      '%s',    '%s',    '%s',    %d,      %d,      '%s',    '%s',    '%s',    '%s',    %d,      %d)
    instup = (lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7], lst[8], lst[9], lst[10], lst[11], lst[12], lst[13], lst[14], lst[15], lst[16], lst[17], lst[18], lst[19], lst[20], lst[21], sex)

    #print lst
    #print instup
    #print insstr % instup 

    res = c.execute(insstr % instup)
    #print res

    #for s in lst[1:-1]:
       #fout.write(s.strip())
       #fout.write(';')
       #print s+";"

    #print "/n"
    #fout.write('\n')
    

def listfile(filename):
    z = pm()
    print '<',
    #fin = open(filename, 'r')
    fin = codecs.open(filename, 'r', encoding='cp1251')
    #print fin.encoding
    #fout = codecs.open(filename+'.copy', 'w+', encoding='cp1251')
    
    #u = unicode('тест','cp1251')
    #fout.write(u)
    
    cnt = 0
    next(fin)
    for ln in fin:
        try:
           ln = ln.replace('\\','\\\\').replace('\'','\\\'')
           processline(ln)
        except:
           print ln
           #print ln.split('|')
           print str(cnt)+" error:", sys.exc_info()

        cnt = cnt + 1
        #if cnt==100:
        #   break
        
        if not cnt % 50000:
           conn.commit()
           print '.',

    fin.close()
    #fout.close()
    print '>'
    print(z)
    print filename, cnt


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
#listfile(u"01.txt")

conn.commit()
conn.close()

