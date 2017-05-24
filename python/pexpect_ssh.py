# coding: utf-8
from pexpect import pxssh
import pexpect

ip = "52.78.94.29"
user = "python"
passwd = "******"
target_file = "/home/python/log.txt"

try:
    s = pxssh.pxssh()
    s.login(ip, user, passwd)
    with open('newlog.txt', 'wb') as f:
        s.logfile = f
        s.sendline('tar -czf /home/python/log.tar.gz '+target_file)
        s.prompt()
        s.logout()
except pxssh.TIMEOUT:
    print('expect timeout')
except pxssh.ExceptionPxssh:
    print('expect password refused')
    
child = pexpect.spawn('scp', [user+'@'+ip+':/home/python/log.tar.gz', '.'])
fout = open('newlog.txt', 'ab')
child.logfile = fout
try:
    child.expect('(?i)password:')
    child.sendline(passwd)
    child.expect(pexpect.EOF)
    fout.close()
except pxssh.EOF:
    print("expect EOF")
except pxssh.TIMEOUT:
    print("expect TIMEOUT")
