#/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
# import json

space = []

df = subprocess.Popen(["df", "-P", "-k"], stdout=subprocess.PIPE)
output = df.communicate()[0]
for line in output.split('\n')[1:]:
    if len(line):
        try:
            device, size, used, avaiable, percent, moutpoint = line.split()
            space.append(dict(moutpoint=moutpoint, avaiable=avaiable, avaiable_per=percent))
        except:
            pass
