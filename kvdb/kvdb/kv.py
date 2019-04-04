import json
import pymysql


class db:
    def __init__(self, database='test'):
        self._db_opts = {'host': '127.0.0.1',
                         'database': database,
                         'autocommit': True,
                         'read_default_file': '~/.my.cnf',
                         'cursorclass': pymysql.cursors.DictCursor}

    def setup(self):
        drop = "DROP TABLE IF EXISTS kvdb"
        create = ("CREATE TABLE kvdb ("
                  "id bigint(20) NOT NULL AUTO_INCREMENT,"
                  "_key varchar(128) NOT NULL,"
                  "_value JSON NOT NULL CHECK (JSON_VALID(_value)),"
                  "PRIMARY KEY (id), UNIQUE KEY (_key)"
                  ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
        self._query(drop)
        self._query(create)

    def _query(self, sql: str):
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

    def dict2json(self, v: dict):
        return(json.dumps(v))

    def str2json(self, v: str):
        f_v = v.replace("'", "\"")
        f_j = json.loads(f_v)
        return f_j

    def get(self, k: dict = None):
        if k is None:
            sql = "SELECT _key,_value FROM kvdb"
        else:
            sql = "SELECT _key,_value FROM kvdb WHERE _key='{}'".format(k)

        rows = self._query(sql)
        if rows:
            for row in rows:
                if '_value' in row:
                    row['_value'] = self.str2json(row['_value'])

        return rows

    def set(self, k: str, v: dict):
        v = self.dict2json(v)
        sql = ("INSERT INTO kvdb (_key, _value) VALUES  ('{k}', '{v}') "
               "ON DUPLICATE KEY UPDATE _value='{v}'").format(k=k, v=v)
        self._query(sql)

    def update(self, k: str, v: dict):
        old_row = self.get(k)
        if old_row:
            value = old_row[0]['_value']
            value.update(v)
            self.set(k, value)
        else:
            return False

    def delete(self, k: str):
        sql = "DELETE FROM kvdb WHERE _key='{}'".format(k)
        self._query(sql)

