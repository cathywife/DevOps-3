#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys

host = sys.argv[1]
user = sys.argv[2]
with open('authorized_keys', 'a') as h:
    with open("./tmp/{host}/home/{user}/.ssh/id_rsa.pub".format(host=host, user=user)) as f:
        h.write(f.read())
