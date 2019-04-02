import json
import pymysql


class db:
    def __init__(self):
        self.result = list()
        self.count = 0
        self._db_opts = {'host': '127.0.0.1',
                         'database': 'test',
                         'autocommit': True,
                         'read_default_file': '~/.my.cnf',
                         'cursorclass': pymysql.cursors.DictCursor}

    def setup(self):
        drop = "DROP TABLE IF EXISTS kvdb"
        create = ("CREATE TABLE kvdb ("
                  "id bigint(20) NOT NULL AUTO_INCREMENT,"
                  "_key varchar(128) NOT NULL,"
                  "_value JSON NOT NULL,"
                  "PRIMARY KEY (id), UNIQUE KEY (_key)"
                  ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
        self._query(drop)
        self._query(create)

    def _query(self, sql):
        con = pymysql.connect(**self._db_opts)
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        con.close()
        if rows:
            return rows
        else:
            return False

    def dict2json(self, v):
        if type(v) is dict:
            return(json.dumps(v))
        else:
            return v

    def str2json(self, v):
        if type(v) is str:
            return json.loads(v.replace("'", "\""))
        elif type(v) is dict:
            return self.dict2json(v)
        else:
            return v

    def get(self, k=None):
        if k is None:
            sql = "SELECT _key,_value FROM kvdb"
        else:
            sql = "SELECT _key,_value FROM kvdb WHERE _key='{}'".format(k)

        rows = self._query(sql)
        for row in rows:
            row['_value'] = self.str2json(row['_value'])

        return rows

    def set(self, k, v):
        v = self.dict2json(v)
        sql = ("INSERT INTO kvdb (_key, _value) VALUES  ('{k}', '{v}') "
               "ON DUPLICATE KEY UPDATE _value='{v}'").format(k=k, v=v)
        self._query(sql)

    def update(self, k, v):
        old_row = self.get(k)
        if old_row:
            value = self.str2json(old_row[0]['_value'])
        else:
            return False

        value.update(v)
        self.set(k, value)
