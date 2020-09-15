-- Engine usage
SELECT count(*),
       engine
FROM information_schema.tables
WHERE table_schema NOT IN ('mysql',
                           'performance_schema',
                           'information_schema')
  AND table_type != 'view'
GROUP BY engine;


-- Tables without indexes
SELECT *
    FROM INFORMATION_SCHEMA.tables
    WHERE table_schema NOT IN ('mysql', 'performance_schema', 'information_schema')
AND table_type != 'view'
  AND TABLE_NAME NOT IN
    (SELECT TABLE_NAME
     FROM
       (SELECT TABLE_NAME,
               index_name
        FROM information_schema.statistics
        WHERE table_schema NOT IN ('mysql', 'performance_schema', 'information_schema')
        GROUP BY TABLE_NAME,
                 index_name) tab_ind_cols
     GROUP BY TABLE_NAME);

-- Count
SELECT count(*), engine FROM information_schema.tables
    WHERE table_schema NOT IN ('mysql', 'performance_schema', 'information_schema')
    AND table_type != 'view' GROUP BY engine;

-- More tables
SELECT * FROM INFORMATION_SCHEMA.tables
    WHERE table_schema NOT IN ('mysql', 'performance_schema', 'information_schema')
AND table_type != 'view'
AND TABLE_NAME NOT IN
    (SELECT TABLE_NAME FROM
        (SELECT TABLE_NAME, index_name
            FROM information_schema.statistics
            WHERE table_schema NOT IN
                ('mysql', 'performance_schema', 'information_schema')
                GROUP BY TABLE_NAME, index_name) tab_ind_cols
            GROUP BY TABLE_NAME);
