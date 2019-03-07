#!/usr/bin/env python3

import pymysql
import argparse


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--old-user', required=True)
    parser.add_argument('--old-host', required=True)
    parser.add_argument('--new-user', required=True)
    parser.add_argument('--new-host', required=True)
    parser.add_argument('--dry-run', action='store_true', default=False)
    args = parser.parse_args()
    old_definer = "'{}'@'{}'".format(args.old_user, args.old_host)
    new_definer = "'{}'@'{}'".format(args.new_user, args.new_host)
    return old_definer, new_definer, args.dry_run


def query(sql, dry_run, print_sql=False):
    if print_sql is True:
        print("{}\n".format(sql))
    if dry_run is True:
        return None
    else:
        rows = None
        db = pymysql.connect(read_default_file='~/.my.cnf',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()
        try:
            cur.execute(sql)
            rows = cur.fetchall()
        finally:
            cur.close()

        if rows:
            return rows
        else:
            return None


def select_from_i_s(table_name, definer):
    d_unquoted = definer.replace("'", "")
    select_sql = "SELECT * FROM information_schema.{t} WHERE DEFINER = \"{d}\""
    return query(sql=select_sql.format(t=table_name, d=d_unquoted), dry_run=False)


def alter_event(definer, event, dry_run):
    print_alter("Altering event {EVENT_SCHEMA}.{EVENT_NAME} definer to {d}".format(d=definer, **event))
    event_sql = ("SET SESSION character_set_client='{CHARACTER_SET_CLIENT}',"
                 "collation_connection='{COLLATION_CONNECTION}';\n"
                 "ALTER "
                 "DEFINER={d} EVENT `{EVENT_SCHEMA}`.`{EVENT_NAME}` "
                 "WHERE DEFINER=\"{d}\" "
                 "ON COMPLETION {ON_COMPLETION};\n").format(d=definer, **event)
    query(sql=event_sql, dry_run=dry_run, print_sql=True)


def alter_view(definer, view, dry_run):
    print_alter("Altering view {TABLE_SCHEMA}.{TABLE_NAME} definer to {d}".format(
        d=definer, **view))
    event_sql = ("SET SESSION character_set_client='{CHARACTER_SET_CLIENT}',"
                 "collation_connection='{COLLATION_CONNECTION}';\n"
                 "ALTER ALGORITHM={ALGORITHM} "
                 "DEFINER={d} "
                 "SQL SECURITY {SECURITY_TYPE} "
                 "VIEW `{TABLE_SCHEMA}`.`{TABLE_NAME}` "
                 "AS {VIEW_DEFINITION};\n").format(d=definer, **view)
    query(sql=event_sql, dry_run=dry_run, print_sql=True)


def alter_trigger(old_definer, new_definer, trigger, dry_run):
    print_alter("Altering trigger {TRIGGER_SCHEMA}.{TRIGGER_NAME} "
                "on {EVENT_OBJECT_SCHEMA}.{EVENT_OBJECT_TABLE} "
                "definer to {d}".format(d=old_definer, **trigger))
    show_create = ("SHOW CREATE TRIGGER `{TRIGGER_SCHEMA}`.`{TRIGGER_NAME}`").format(**trigger)
    old_trigger = query(show_create, dry_run=False, print_sql=False)[0]['SQL Original Statement']
    new_trigger = old_trigger.replace("CREATE DEFINER={}".format(old_definer),
                                      "CREATE DEFINER={}".format(new_definer))
    trigger['ddl'] = new_trigger
    trigger_sql = (
        "SET SESSION character_set_client='{CHARACTER_SET_CLIENT}',"
        "collation_connection='{COLLATION_CONNECTION}',"
        "sql_mode={SQL_MODE};\n"
        "LOCK TABLE `{EVENT_OBJECT_SCHEMA}`.`{EVENT_OBJECT_TABLE}` WRITE;\n"
        "DROP TRIGGER `{TRIGGER_SCHEMA}`.`{TRIGGER_NAME}`;\n"
        "{ddl};\n"
        "UNLOCK TABLE `{EVENT_OBJECT_SCHEMA}`.`{EVENT_OBJECT_TABLE}`;\n"
    ).format(**trigger)
    query(sql=trigger_sql, dry_run=dry_run, print_sql=True)


def alter_routine(old_definer, new_definer, routine, dry_run):
    print_alter("Altering {ROUTINE_TYPE} {ROUTINE_SCHEMA}.{ROUTINE_NAME}".format(**routine))
    show_create = ("SHOW CREATE {ROUTINE_TYPE} `{ROUTINE_SCHEMA}`.`{ROUTINE_NAME}`").format(**routine)
    old_routine = query(show_create, dry_run=False, print_sql=False)
    k = "Create {}".format(routine['ROUTINE_TYPE'].title())
    routine_ddl = old_routine[0][k]
    routine_ddl.replace("CREATE DEFINER={}".format(old_definer),
                        "CREATE DEFINER={}".format(new_definer))
    routine['ddl'] = routine_ddl
    routine_sql = (
        "SET SESSION character_set_client='{CHARACTER_SET_CLIENT}',"
        "collation_connection='{COLLATION_CONNECTION}',"
        "sql_mode={SQL_MODE};\n"
        "DELIMITER $$\n"
        "DROP {ROUTINE_TYPE} `{ROUTINE_SCHEMA}`.`{ROUTINE_NAME}` $$\n"
        "{ddl} $$\n"
        "DELIMITER ;\n"
    ).format(**routine)
    query(sql=routine_sql, dry_run=dry_run, print_sql=True)


def print_alter(msg):
    print("--\n-- {}\n--\n".format(msg))


if __name__ == "__main__":
    OLD, NEW, DRY_RUN = args()
    OLD_SQL = OLD.replace("'", "`")
    NEW_SQL = NEW.replace("'", "`")
    VIEWS = select_from_i_s("VIEWS", OLD)
    TRIGGERS = select_from_i_s("TRIGGERS", OLD)
    EVENTS = select_from_i_s("EVENTS", OLD)
    PROCEDURES = select_from_i_s("ROUTINES", OLD)

    if VIEWS:
        for v in VIEWS:
            alter_view(definer=NEW_SQL, view=v, dry_run=DRY_RUN)
    if TRIGGERS:
        for t in TRIGGERS:
            alter_trigger(old_definer=OLD, new_definer=NEW, trigger=t,
                    dry_run=DRY_RUN)
    if EVENTS:
        for e in EVENTS:
            alter_event(NEW, e, DRY_RUN)
    if PROCEDURES:
        for p in PROCEDURES:
            alter_routine(OLD, NEW, p, DRY_RUN)

