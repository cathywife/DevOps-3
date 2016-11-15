
# -*- coding:utf-8 -*-
from fabric.api import *

env.user = "web"
env.hosts = ['10.150.10.203', '10.150.20.203']
env.password = "web"

@runs_once
def input_raw():
    return prompt("please input directory name:", default="/home")

def worktask(dirname):
    run("ls -l "+dirname)

@task
def go():
    getdirname = input_raw()
    worktask(getdirname)

