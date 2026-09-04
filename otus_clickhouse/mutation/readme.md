1.  
CREATE TABLE `default`.user_activity
(
user_id UInt32,
activity_type String,
activity_date DateTime
)
Engine = MergeTree()
PARTITION BY toYYYYMMDD(activity_date)

INSERT INTO `default`.user_activity VALUES (1 , 'login','2026-09-04 12:00:00'),(2 , 'logout','2026-09-03 12:00:00'),
(3 , 'purchase','2026-09-02 12:00:00')
[1.png]

2.  
ALTER TABLE `default`.user_activity UPDATE activity_type = 'logout' WHERE 1=1;
[2.png]

3.  SELECT * FROM "default"."user_activity"
[3.png]

SELECT
    database,
    table,
    mutation_id,
    command,
    create_time,
    parts_to_do,
    is_done
FROM system.mutations
ORDER BY create_time DESC;
[4.png]

4.  SELECT DISTINCT _partition_value AS partition
    FROM `default`.user_activity
    ORDER BY partition ASC;
[5.png]

    ALTER TABLE `default`.user_activity DROP PARTITION '20260902';
[6.png], [7.png]

SELECT * FROM "default"."user_activity" LIMIT 100
[8.png]
Данные удалились!!!!