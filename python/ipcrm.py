#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
这个脚本用于清除osma占用的无效共享内存
"""
import os, time
result = os.popen("""ipcs -s|awk '{if($3=="zabbix")if($1=="0x00000000")print $2}'""")
tmp = result.read()
tmp = tmp.strip()
zabbix_list = []
for item in tmp.split('\n'):
    zabbix_list.append(item)

time.sleep(2)

result2 = os.popen("""ipcs -s|awk '{if($3=="zabbix")if($1=="0x00000000")print $2}'""")
tmp2 = result2.read()
tmp2 = tmp2.strip()

for zabbix in tmp2.split('\n'):
    if zabbix in zabbix_list:
        # print(zabbix)
        os.system("ipcrm -s %s" % zabbix)
