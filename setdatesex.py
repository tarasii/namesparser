# -*- encoding: cp1251 -*-
# cp1251 

import time
import datetime
import os
import codecs
import sys

reload(sys)
sys.setdefaultencoding('cp1251')

sys.stdout = codecs.getwriter('cp866')(sys.stdout,'replace')

import mysql.connector

upd_cmd = "UPDATE people SET birthday = '%s', sex = '%s' WHERE id = %d;"

def proces_srow(cu, row):
    #ci = conn.cursor()
    idn = row[0]
    inn = row[1]
    curd = row[2]

    if len(curd)==10:
        newd = curd[6:10] + curd[3:5] + curd[0:2]
    else:
        newd = '00000000'

    if int(inn[8])% 2 == 0:
        sex = u'Ж'
    else:
        sex = u'М'

    cmd_str = upd_cmd % (newd, sex, idn)
    
    try:
       cu.execute(cmd_str)
    except:
       print cmd_str

    #cu.execute(upd_cmd, (newd, sex, idn))
    #ci.close()

    #print cmd_str

print "start"

conn  = mysql.connector.connect(user='root', password='root123',
                              host='127.0.0.1',
                              database='test', charset='cp1251')

connupd  = mysql.connector.connect(user='root', password='root123',
                              host='127.0.0.1',
                              database='test', charset='cp1251')

c = conn.cursor()
cu = connupd.cursor()
c.execute("SELECT id, tax_number, birthday_str, sex from people WHERE ISNULL(sex) = 1;")

cnt = 1
row = c.fetchone()
while row is not None:
   proces_srow(cu, row)
   row = c.fetchone()

   if not cnt % 55000:
      connupd.commit()
      print '.',

   if not cnt % 2000000:
      print ''

   cnt += 1


cu.close()
connupd.commit()
connupd.close()

c.close()
conn.close()



