# -*- coding:utf-8 -*-
from fabric.api import local, cd, run, env, \
                            hosts, task, put, sudo, parallel
from config import Hosts

env.hosts = Hosts.hosts
env.password = Hosts.passwd
env.user = "web"
# now = time.strftime("%Y%m%d%H")
# code_tag = "appserver.%s.gz"%now
code_tag = "appserver.gz"


@task
def df():
    run("df -h")


@task
def check():
    run("ps aux| grep uwsgi | grep imgstore | grep -v grep | wc -l")


@task
def checkconf():
    run("cat ~/webhive/conf/uwsgi/apps-available/shownail.ini | grep processes")


@task
@parallel
def push():
    '''部署代码'''
    put(code_tag, Hosts.workspace)
    with cd(Hosts.workspace):
        run("tar xzvf %s" % code_tag)
        run("cp ~/webhive/appserver/MAShow/mashow/settings.pro.py ~/webhive/appserver/MAShow/mashow/settings.py")
        run("cp ~/webhive/appserver/ImgStore/ImgStore/settings.pro.py ~/webhive/appserver/ImgStore/ImgStore/settings.py")


@task
@parallel
def restart():
    '''重启服务'''
    sudo(Hosts.execute_restart)
    run("ps aux| grep uwsgi | grep shownail | grep -v grep | wc -l")


@task
def tag():
    '''打包代码'''
    local("tar -zcvf %s appserver/" % code_tag)


@task
@parallel
def secure():
    '''部署secure项目'''
    # run("mkdir -p ~/webhive/secure/")
    # run("mkdir -p ~/webhive/run/uwsgi/secure/")
    run("cp -r ~/webhive/appserver/MAShow/* ~/webhive/secure/MAShow/")
    sudo(Hosts.secure_restart)
    run("ps aux| grep uwsgi | grep secure | grep -v grep | wc -l")


@task
@hosts('42.62.65.26')
def async():
    '''部署异步任务代码自动化发布程序主入口'''
    put(code_tag, Hosts.workspace)
    with cd(Hosts.workspace):
        run("tar xzvf %s" % code_tag)
        run("cp ~/webhive/appserver/MAShow/mashow/settings.pro.py ~/webhive/appserver/MAShow/mashow/settings.py")
        run("cp ~/webhive/appserver/ImgStore/ImgStore/settings.pro.py ~/webhive/appserver/ImgStore/ImgStore/settings.py")
        run("supervisorctl -c /home/web/webhive/conf/supervisor/supervisord.conf restart all")


@task
@hosts('42.62.65.26')
def apptest(project='appserver_test'):
    code_test_tag = "appserver_test.gz"
    local("tar -zcvf %s %s/" % (code_test_tag, project))
    put(code_test_tag, Hosts.workspace)
    with cd(Hosts.workspace):
        run("tar xzvf %s" % code_test_tag)
        run("cp ~/webhive/%s/MAShow/mashow/settings.pro.py"
                " ~/webhive/appserver_test/MAShow/mashow/settings.py" % (project))
        run("touch ~/webhive/appserver_test.VERSION")


@task
@hosts('42.62.65.26')
def opentest(project='open_orders'):
    code_test_tag = "open_orders.gz"
    local("tar -zcvf %s %s/" % (code_test_tag, project))
    put(code_test_tag, Hosts.workspace)
    with cd(Hosts.workspace):
        run("tar xzvf %s" % code_test_tag)
        run("cp ~/webhive/%s/MAShow/mashow/settings.pro.py"
                " ~/webhive/%s/MAShow/mashow/settings.py" % (project, project))
        run("touch ~/webhive/open_orders.VERSION")


@task
@hosts('42.62.65.26')
def searchtest():
    code_test_tag = "search_box.gz"
    local("tar -zcvf %s search_box/" % code_test_tag)
    put(code_test_tag, Hosts.workspace)
    with cd(Hosts.workspace):
        run("tar xzvf %s" % code_test_tag)
        run("cp /home/web/webhive/search_box/searchbox/SearchBox/SearchBox/settings_pro.py"
            " ~/webhive/search_box/searchbox/SearchBox/SearchBox/settings.py")
        run("touch ~/webhive/search_box.VERSION")


@task
@hosts('42.62.65.26')
def paytest(project='payment_service'):
    code_test_tag = "payment_service.gz"
    local("tar -zcvf %s %s/" % (code_test_tag, project))
    put(code_test_tag, Hosts.workspace)
    with cd(Hosts.workspace):
        run("tar xzvf %s" % code_test_tag)
        run("cp ~/webhive/%s/MAShow/mashow/settings.pro.py"
                " ~/webhive/%s/MAShow/mashow/settings.py" % (project, project))
        run("touch ~/webhive/payment_service.VERSION")
