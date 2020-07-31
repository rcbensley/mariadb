import pymysql
import argparse
from time import sleep

DB_ARGS = {"host": "127.0.0.1",
           "port": 3306,
           "database": "mysql",
           "cursorclass": pymysql.cursors.DictCursor}


SQL_SHOW_MASTER = "SHOW MASTER STATUS;"
SQL_SHOW_SLAVE = "SHOW SLAVE STATUS;"


def query(sql, args: dict=DB_ARGS):
    sleep(8)
    db = pymysql.connect(**args)
    cur = db.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    finally:
        cur.close()

    if len(rows) == 0:
        return None
    elif len(rows) == 1:
        return rows[0]
    else:
        return rows

def p(header, lines):
    print(header)
    for l in lines:
        print("{:}{:>32}".format(l[0] + ":", l[1]))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--user', '-u', required=True)
    parser.add_argument('--password', '-p', required=True)
    args = parser.parse_args()
    db_conn_args = DB_ARGS.copy()
    db_conn_args['user'] = args.user
    db_conn_args['password'] = args.password

    master_status = query(sql=SQL_SHOW_MASTER, args=db_conn_args)
    slave_status = query(sql=SQL_SHOW_SLAVE, args=db_conn_args)

    if master_status is None:
        print("I am not a master")
    else:
        ms_lines = (("File", master_status['File']),
                ("Pos", master_status['Position']),)
        p("Local Master Info", ms_lines)

    if slave_status is None:
        print("I am not a slave")
    else:
        ss_lines = (("Host", slave_status['Master_Host']),
                ("Port", slave_status['Master_Port']),
                ("File", slave_status['Master_Log_File']),
            ("Pos", slave_status['Exec_Master_Log_Pos']),)
        p("Remote Master Info:", ss_lines)

