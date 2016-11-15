
# -*- coding:utf-8 -*-
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
import time
import os

env.user = "web"
env.hosts = ['**.**.**.**']
env.password = "******"

env.dev_root = "/home/web/webhive"
env.dev_source = "appserver"
env.dev_releases = "releases"

env.deploy_root = "/home/web/webhive"
env.deploy_current = "appserver"
env.deploy_releases = "releases"
env.deploy_version = time.strftime("%Y%m%d_%H%M")


@task
def df():
    '''查看磁盘'''
    run("df -h")

@task
@runs_once
def old_version():
    '''获取当前版本号'''
    with cd(env.deploy_root):
        result = os.popen('ls -l %s' % env.deploy_current)
        result1 = result.read()
        old_version = result1.split('/')[1].strip()
        return old_version


@task
@runs_once
def tag():
    '''打包源码'''
    print yellow("Creating source package...")
    with lcd(env.dev_root):
        local("tar -czf %s/%s.tar.gz %s" %
            (env.dev_releases, env.deploy_version, env.dev_source))
    print green("Creating source package success!")


def push_package():
    '''上传代码'''
    print yellow("Start put package...")
    with cd(env.deploy_root):
        run("mkdir -p %s" % env.deploy_releases)
    result = put(env.dev_root + env.dev_releases +
        env.deploy_version + ".tar.gz", env.deploy_root +
        env.deploy_releases + env.deploy_version + '.tar.gz')
    if result.failed and not("put file failed, Continue[Y/N]?"):
        abort("Aborting file put task!")


def untar_mklink():
    '''部署代码【解压与软连】'''
    print yellow("update current symlink")
    with cd(env.deploy_root + env.deploy_releases):
        run("tar -xzvf %s.tar.gz" % env.deploy_version)
        run("mv %s %s" % (env.dev_source, env.deploy_version))
    with cd(env.deploy_root):
        run("rm -rf %s" % env.deploy_current)
        run("ln -s %s/%s %s" % (env.deploy_releases, env.deploy_version,
            env.deploy_current))
    print green("make symlink success!")


@task
def restart():
    '''重启服务'''
    print yellow("restart uwsgi service")
    sudo("touch ~/webhive/appserver.VERSION")
    run("ps aux| grep uwsgi | grep shownail | grep -v grep | wc -l")
    print green("uwsgi service restart success!")


@task
def rollback():
    '''代码回滚'''
    print yellow("rollback project version...")
    old_version()
    if old_version == "":
        abort("old version empty, abort!")
    with cd(env.deploy_root):
        run("rm -rf %s" % env.deploy_current)
        run("ln -s %s/%s %s" % (env.deploy_releases, old_version,
            env.deploy_current))
    restart_service()
    print green("rollback success!")


@task
def deploy():
    '''自动化发布程序'''
    tag()
    push_package()
    untar_mklink()
    restart()
