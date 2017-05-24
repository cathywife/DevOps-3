# coding: utf-8
import paramiko
hostname = "10.150.10.203"
username = "web"
password = "web"
paramiko.util.log_to_file('log_paramiko.log')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname, username=username, password=password)
stdin, stdout, stderr = ssh.exec_command('free -m')
stdout = stdout.read()
print(stdout.decode('utf-8'))
ssh.close()
