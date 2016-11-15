
# -*- coding:utf-8 -*-
from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm

env.user = "web"
env.hosts = ['10.150.10.203', '10.150.20.203']
env.password = "web"

@task
@runs_once
def tar_task():
    with lcd('/home/test'):
        local("tar -czf wget.tar.gz wget.log")

@task
def put_task():
    run("mkdir -p data/logs")
    with cd("data/logs"):
        with settings(warn_only=True):
            result = put("/home/test/wget.tar.gz", "/home/web/data/logs/wget.tar.gz")
        if result.failed and not confirm("put file failed, Continue[Y/N]?"):
            abort("Aborting file put task!")

@task
def check_task():
    with settings(warn_only=True):
        lmd5 = local("md5sum /home/test/wget.tar.gz", capture=True).split(' ')[0]
        rmd5 = run("md5sum /home/web/data/logs/wget.tar.gz").split(' ')[0]
    if lmd5 == rmd5:
        print("OK")
    else:
        print("ERROR")

@task
def go():
    tar_task()
    put_task()
    check_task()

