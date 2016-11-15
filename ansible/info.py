
# -*- coding: utf-8 -*-
import json
import shlex
import sys

DOCUMENTATION = '''
---
module: info
short_description: This modules is extend facts modules
description:
    - This modules is extend facts modules
version_added: "1.1"
options:
    enable:
        description:
            - enable extend facts
        required: true
        default: null
'''

EXAMPLES = '''
- info: enable=yes
'''

args_file = sys.argv[1]
args_data = open(args_file).read()
arguments = shlex.split(args_data)
for arg in arguments:
    if "=" in arg:
        (key, value) = arg.split("=")
        if key == "enable" and value == "yes":
            data = {}
            data['key'] = value
            data['list'] = ['one', 'two', 'three']
            data['dict'] = {'A': "a"}
            print(json.dumps({"ansible_facts": data}, indent=4))
        else:
            print("info modules usage error")
    else:
        print("info modules need one parameter")
