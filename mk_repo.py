# coding: utf-8
# from urllib import request
import urllib2
import paramiko
import os

repo = 'CentOS6.repo'
username = "root"
password = "123456"
hosts = ['192.168.99.103', '192.168.99.105']

# Download 163 repository
# f = request.urlopen('http://mirrors.163.com/.help/CentOS6-Base-163.repo')
f = urllib2.urlopen('http://mirrors.163.com/.help/CentOS6-Base-163.repo')
data = f.read()
with open(repo, 'wb') as code:
    code.write(data)

# Change some item in yum repository file
lines = open(repo, 'r+').readlines()
lines_new = []
for line in lines:
    line = line.replace('$releasever', '6')
    lines_new.append(line)
open(repo, 'w+').writelines(lines_new)

# Upload yum file to remote host
for host in hosts:
    t = paramiko.Transport((host))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(repo, '/etc/yum.repos.d/' + repo)
    t.close()
os.remove(repo)

