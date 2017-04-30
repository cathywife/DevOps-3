#!/usr/bin/python
"""
Description: This lookup query value from PostgreSQL
Example Usage:
{{ lookup('psql', ('192.168.1.117', 'ansible', 'lookup', 'ansible'))}}
"""
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
HAVE_PSQL = False
try:
    import psycopg2
    HAVE_PSQL = True
except ImportError:
    pass

class LookupModule(LookupBase):
    """docstring for LookupModule"""
    def run(self, terms, variables, **kwargs):
        if HAVE_PSQL is False:
            raise AnsibleError("Can't LOOKUP(psql):"
                "module psycopg2 is not installed")

        ret = []
        for term in terms:
            host, db, table, key = (term[0], term[1], term[2], term[3])
            conn = psycopg2.connect(database=db, user='postgres',
                password='123456', host=host)
            cur = conn.cursor()
            sql = "select date from %s where hosts = '%s'" % (table, key)
            cur.execute(sql)
            result = cur.fetchone()
            cur.close()
            conn.close()
        if result[0]:
            ret.append(result[0])
            return ret
        else:
            return None
