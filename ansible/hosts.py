# -*- coding:utf-8 -*-

import argparse
import json

def lists():
    r = {}
    h = ['192.168.99.11' + str(i) for i in range(0, 2)]
    n = ['192.168.99.11' + str(i) for i in range(0, 2)]
    var_web = {'ansible_ssh_user': 'web'}
    var_db = {'ansible_ssh_user': 'db'}
    var_simple = {'ansible_ssh_user': 'python', 'ansible_ssh_pass': '******'}
    r['webserver'] = {'hosts': h, 'vars': var_web}
    r['dbserver'] = {'hosts': n, 'vars': var_db, "children": ["simple"]}
    r['simple'] = {'hosts': ['1.1.1.1'], 'vars': var_simple}
    r['solo'] = ['192.168.99.102']
    return json.dumps(r, indent=4)

def hosts(name):
    r = json.loads(lists())
    for i in r.keys():
        if isinstance(r[i], list):
            if name in r[i]:
                return json.dumps({})
        elif isinstance(r[i], dict):
            if name in r[i]['hosts']:
                return json.dumps(r[i]['vars'], indent=4)
    else:
        return "Unkown host"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help='hosts list', action='store_true')
    parser.add_argument('-H', '--host', help='host vars')
    args = vars(parser.parse_args())

    if args['list']:
        print(lists())
    elif args['host']:
        print(hosts(args['host']))
    else:
        print(parser.print_help())
