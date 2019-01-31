from pymysql import connect

sql = "SELECT @@version;"
conn = connect(read_default_file="~/.my.cnf")
cur = conn.cursor()
try:
    cur.execute(sql)
    rows = list(cur.fetchall())
finally:
    conn.close()

print(rows[0][0])

