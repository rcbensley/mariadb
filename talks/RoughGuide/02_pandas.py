# Python 3.5+

import pandas
import configparser
import sys
from pathlib import Path

my_cnf_path = str(Path.home()) + "/.my.cnf"
client_cnf = configparser.ConfigParser()
client_cnf.read(my_cnf_path)
client_user = client_cnf['client']['user']
client_password = client_cnf['client']['password']

df_titles_con = f"mysql+pymysql://{client_user}:{client_password}@localhost/employees"

df_titles_sql = ("SELECT e.emp_no, "
                 "e.first_name, "
                 "e.last_name, "
                 "de.from_date, "
                 "de.to_date, "
                 "d.dept_name "
                 " FROM employees e"
                 " INNER JOIN dept_emp de"
                 " ON e.emp_no = de.emp_no"
                 " INNER JOIN departments d"
                 " ON de.dept_no = d.dept_no")

df_titles = pandas.read_sql_query(df_titles_sql, df_titles_con)
print(df_titles.head())
