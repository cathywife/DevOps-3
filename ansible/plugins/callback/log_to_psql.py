#!/usr/bin/env python

import psycopg2
import datetime
from ansible.plugins.callback import CallbackBase
import json

class CallbackModule(CallbackBase):
    TIME_FORMAT = '%b %d %Y %H:%M:%S'
    now = datetime.datetime.now()

    def __init__(self):
        super(CallbackModule, self).__init__()

    def insert(self, host, res):
        conn = psycopg2.connect(database='ansible', user='postgres',
            password='123456', host='127.0.0.1')
        cur = conn.cursor()
        sql = "insert into status(hosts, result, date) values('%s', '%s', '%s')"%\
            (host, json.dumps(res), self.now.strftime(self.TIME_FORMAT))
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.insert(host, res)

    def runner_on_ok(self, host, res):
        self.insert(host, res)

    def runner_on_unreachable(self, host, res):
        self.insert(host, res)

    def playbook_on_stats(self, stats):
        hosts = stats.processed.keys()
        for i in hosts:
            info = stats.summarize(i)
            if info['failures'] > 0 or info['unreachable'] > 0:
                has_errors = True
            msg = "Hosinfo: %s, ok: %d, failures: %d, unreachable:"\
                "%d, changed: %d, skipped: %d" % (i, info['ok'], info['failures'],
                    info['unreachable'], info['changed'], info['skipped'])
            print(msg)
