
# -*- coding:utf-8 -*-
from fabric.colors import *
from fabric.api import *
env.user = 'web'
env.roledefs = {
    'server1': ['10.150.10.203'],
    'server2': ['10.150.20.203']
}
env.passwords = {
    'web@10.150.10.203': 'web',
    'web@10.150.20.203': 'web'
}

@roles('server1')
def server1_task():
    print yellow("run something in server1...")
    with settings(warn_only=True):
        run("/sbin/ifconfig")
        run("touch server103")

@roles('server2')
def server2_task():
    print yellow("run something in server2...")
    with settings(warn_only=True):
        run("/sbin/ifconfig")
        run("touch server203")

@roles('server1', 'server2')
def public_task():
    print yellow("touch some file")
    with settings(warn_only=True):
        run("touch 103203")

def deploy():
    execute(public_task)
    execute(server1_task)
    execute(server2_task)

