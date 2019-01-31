import json

json_file = "./json_sql_opts.json"

if sql_opts:
    json.dump(sql_opts, open(json_file, 'w'))

def json_format_sql(sql, json_file_path=json_file):
    opts = json.load(open(json_file_path, 'r'))
    print(opts)
    s = sql.format(**opts)
    print(s)
    return s

if sql:
    json_format_sql(sql)

