#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from fabric.api import local, cd, run, env, lcd,\
    hosts, task, put, sudo, parallel, runs_once
from fabric.colors import *
from fabric.context_managers import *
import time, os


env.user = "python"
env.hosts = ['*.*.*.*']
env.password = "******"

env.dev_root = 'e:'
env.dev_source = "mysite"
env.dev_releases = "releases"

env.deploy_root = "/home/python/webhive/appserver"
env.deploy_current = "mysite"
env.deploy_releases = "releases"
env.deploy_version = time.strftime("%Y%m%d_%H%M%S")
env.version_filename = "old_versionID"


@task
def df():
    '''产看磁盘'''
    run('df -h')


@task
@runs_once
def get_versionID():
    """获取线上运行版本号"""
    with cd(env.deploy_root):
        versionID = run("ls -l %s|awk -F '/' '{print $2}'"
            % env.deploy_current)
    return versionID

@task
@runs_once
def tag():
    '''本地代码打包'''
    print yellow("Creating source package...")
    # windows下不在同一驱动器需要手动变更
    os.chdir(env.dev_root)
    with lcd(env.dev_root):
        if not os.path.isdir(env.dev_releases):
            local("mkdir %s" % env.dev_releases)
    with lcd(env.dev_root):
        local("tar -czf %s/%s.tar.gz %s" %
            (env.dev_releases, env.deploy_version, env.dev_source))

def push_package():
    """上传代码"""
    print yellow("Start put package...")
    with cd(env.deploy_root):
        run("mkdir -p %s" % env.deploy_releases)
    src = os.path.join(env.dev_root, env.dev_releases, env.deploy_version + ".tar.gz")
    dest = env.deploy_root + '/' + env.deploy_releases + '/' + env.deploy_version + ".tar.gz"
    result = put(src, dest)
    if result.failed and not("put file failed, Continue[Y/N]?"):
        abort("Aborting task of put package!")

def deploy_package():
    """部署代码【解压和软连】"""
    print yellow("update current symlink")
    releases_path = env.deploy_root + '/' + env.deploy_releases
    with cd(releases_path):
        run("tar -xzf %s.tar.gz" % env.deploy_version)
        run("mv %s %s" % (env.dev_source, env.deploy_version))
    with cd(env.deploy_root):
        run_version = run("ls -l %s|awk -F '/' '{print $2}'"
            % env.deploy_current)
        run("echo %s > %s/%s" % (run_version, env.deploy_releases, env.version_filename))
        run("rm -rf %s" % env.deploy_current)
        run("ln -s %s/%s %s" % (env.deploy_releases,
            env.deploy_version, env.deploy_current))
    print green("create new symlink success!")


@task
def restart_service():
    """重启服务"""
    print yellow("restat uwsgi service")
    sudo("touch ~/webhive/appserver.VERSION")
    run("ps aux|grep uwsgi|grep -v grep|wc -l")
    print green("uwsgi service restart success!")

@task
def rollback():
    """代码回滚"""
    print yellow("rollback project version...")
    with cd(env.deploy_root):
        old_version = run('cat %s/%s' % (env.deploy_releases, env.version_filename))
        if old_version == "":
            abort("old version is empty, abort!")
        run("rm -rf %s" % env.deploy_current)
        run("ln -s %s/%s %s" % (env.deploy_releases,
            old_version, env.deploy_current))
    restart_service()
    print green("rollback success!")

@task
def deploy():
    """自动化发布程序"""
    tag()
    push_package()
    deploy_package()
    restart_service()

