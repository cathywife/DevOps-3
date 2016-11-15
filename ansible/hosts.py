
# -*- coding:utf-8 -*-
import argparse
import json
# import sys


def lists():
    r = {}
    h = ['172.17.42.10' + str(i) for i in range(1, 4)]
    hosts = {'hosts': h}
    r['docker'] = hosts
    return json.dumps(r, indent=4)


def hosts(name):
    r = {'ansible_ssh_pass': '123456'}
    cpis = dict(r.items())
    return json.dumps(cpis)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help="hosts list", action='store_true')
    parser.add_argument('-H', '--host', help='host vars')
    args = vars(parser.parse_args())

    if args['list']:
        print(lists())
    elif args['host']:
        print(hosts(args['host']))
    else:
        parser.print_help()
