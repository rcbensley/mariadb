import pymysql
import json
import csv


def query(sql):
    c = pymysql.connect(read_default_file="~/.my.cnf")
    cur = c.cursor()
    cur.execute(sql)
    r = cur.fetchall()
    cur.close()
    c.close()
    if r:
        if len(r[0]) == 1:
            # Return only the first 'column' of each row
            rows = list([c[0] for c in r])
            return rows
        else:
            return r


def rows_to_csv(rows, target):
    with open(target, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in rows:
            csv_writer.writerow(row)


def important_daily_batch_job(source, target):
    rows = query(source)
    rows_to_csv(rows, target)


def run_import_daily_job_jobs(jobs):
    for job in jobs:
        important_daily_batch_job(**job)


def jobs_to_json(job_strings):
    daily_jobs_json = []
    for j in daily_job_strings:
        job_string_as_json = json.loads(j)
        daily_jobs_json.append(job_string_as_json)
    return daily_jobs_json

# GO!
get_jobs_sql = "select JSON_OBJECT('source', source, 'target', target) FROM jobs.dailies"
daily_job_strings = query(get_jobs_sql)

def go():
    j = jobs_to_json(daily_job_strings)
    run_import_daily_job_jobs(j)

go()
