1. Создадим таблицу monitoring.main_table которая получает все значения Background и сравнивает с максимальным 
insert into monitoring.main_table
WITH
    tasks AS (
        SELECT
            replaceRegexpOne(metric, 'PoolTask$', '') AS pool_prefix,
            value AS active_tasks
        FROM system.metrics
        WHERE metric LIKE '%PoolTask'
    ),
    sizes AS (
        SELECT
            replaceRegexpOne(metric, 'PoolSize$', '') AS pool_prefix,
            value AS max_size
        FROM system.metrics
        WHERE metric LIKE '%PoolSize'
    )
SELECT
    t.pool_prefix AS pool_name,
    s.max_size,
    t.active_tasks,
    if(s.max_size > 0, round(t.active_tasks / s.max_size * 100, 2), 0) AS fill_percent,
    now()
    
FROM tasks t
INNER JOIN sizes s ON t.pool_prefix = s.pool_prefix
ORDER BY fill_percent DESC;
[1.png]
2. Создаем чарт во встроенном дашборде
[2.png][3.png]
Правый нижний угол на картинке