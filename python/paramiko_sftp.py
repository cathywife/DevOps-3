# coding: utf-8
import paramiko
username = "web"
password = "web"
hostname = "10.150.10.203"
try:
    t = paramiko.Transport((hostname))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put('pexpect_ssh.py', 'pexpect_test.py')
    sftp.get('head.jpg', 'new.jpg')
    sftp.mkdir('./testaaa')
    sftp.rmdir('./testbbb')
    sftp.rename('pexpect_test.py', 'pexpect_test1.py')
    print(sftp.stat('head.jpg'))
    print(sftp.listdir('.'))
    t.close()
except Exception as e:
    print(str(e))
    
