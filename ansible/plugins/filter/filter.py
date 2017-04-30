#!/usr/bin/python
# from jinja2.filters import environmentfilter
# rom ansible import errors
import time

# change str to list
def string(str, seperator=' '):
    return str.split(seperator)

# change datetime to timestamp
def _time(times):
    return time.mktime(time.strptime(times, '%Y-%m-%d %H:%M:%S'))

class FilterModule(object):
    ''' Ansible custom filter'''
    def filters(self):
        return {
            'sep': string,
            'timep': _time,
        }
