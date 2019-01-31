from datetime import datetime as dt

sql = "SELECT {columns} FROM {database}.{table} {where} {outfile}"

sql_opts = {"columns": "*",
        "database": "employees",
        "table": "salaries",
        "where": "",
        "date": dt.today().strftime("%Y-%m-%d"),
        "outfile": "INTO OUTFILE '/tmp/{database}_{table}_{date}.tsv'"}

sql_opts["outfile"] = sql_opts["outfile"].format(**sql_opts)


def format_sql(sql, opts):
    formatted_sql = sql.format(**opts)
    print(formatted_sql)
    return formatted_sql

format_sql(sql=sql, opts=sql_opts)

