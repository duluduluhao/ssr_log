# -*- coding: utf-8 -*-
import re
import sqlite3
#说明
print 'V0.0.2'

#读取日志文件、连接数据库

log_db = sqlite3.connect('./log.db')
cursor = log_db.cursor()
#建表
cursor.execute('DROP TABLE IF EXISTS SSR_LOG')
cursor.execute("CREATE TABLE SSR_LOG (id INT  PRIMARY KEY  NOT NULL, log_date, ip_addr,http_addr)")

print "Table created successfully"

cursor.execute("INSERT INTO SSR_LOG (id, log_date, ip_addr,http_addr) VALUES (0,'2018.1.1','192.168.1.1','www.google.com')")
#设定正则规则
data_re = re.compile(r'(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)')
ip_re = re.compile(r'((?:(?:25[0-5]|2[0-4]\d|(?:1\d{2}|[1-9]?\d))\.){3}(?:25[0-5]|2[0-4]\d|(?:1\d{2}|[1-9]?\d)))')
http_re = re.compile(r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
#读取日志文件
shadowsockslog = open('./shadowsocks.log')
index = 0
#进行转换
for line in shadowsockslog:

    log_date_t = data_re.search(line)

    ip_addr_t = ip_re.search(line)

    http_addr_t_start = line.find("connecting")
    http_addr_t_end = line.find("from")
    http_addr_t = ""

    if (http_addr_t_start != -1) and (http_addr_t_end != -1):
        http_addr_t = line[http_addr_t_start+11:http_addr_t_end-5]

   # print type(log_date_t),type(ip_addr_t),type(http_addr_t),type(line)
    print line

    if log_date_t != None and ip_addr_t != None and http_addr_t != None:
        index = index + 1
        data = (index,log_date_t.group(0),ip_addr_t.group(0),http_addr_t)
        sqlite3_command = "INSERT INTO SSR_LOG values(?,?,?,?)"
        cursor.execute(sqlite3_command,data)
        print "(%d)::%s,%s,%s" % (index,log_date_t.group(0),ip_addr_t.group(0),http_addr_t)

print 'job done! index(%d)' % index

p_cursor = cursor.execute("SELECT id, log_date, ip_addr, http_addr  from SSR_LOG")


for row in p_cursor:
   print "ID = ", row[0]
   print "log_date = ", row[1]
   print "ip_addr = ", row[2]
   print "http_addr = ", row[3], "\n"

print "Operation done successfully";
log_db.close()




