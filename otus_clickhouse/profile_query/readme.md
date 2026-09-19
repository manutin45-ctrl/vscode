1. создадим тестовую таблицу
CREATE TABLE profile_query.sensors
(
    sensor_id UInt16,
    sensor_type Enum('BME280', 'BMP180', 'BMP280', 'DHT22', 'DS18B20', 'HPM', 'HTU21D', 'PMS1003', 'PMS3003', 'PMS5003', 'PMS6003', 'PMS7003', 'PPD42NS', 'SDS011'),
    location UInt32,
    lat Float32,
    lon Float32,
    timestamp DateTime,
    P1 Float32,
    P2 Float32,
    P0 Float32,
    durP1 Float32,
    ratioP1 Float32,
    durP2 Float32,
    ratioP2 Float32,
    pressure Float32,
    altitude Float32,
    pressure_sealevel Float32,
    temperature Float32,
    humidity Float32,
    date Date MATERIALIZED toDate(timestamp)
)
ENGINE = MergeTree
ORDER BY (timestamp, sensor_id);
2. Вставим данные (тестовый датасет: https://clickhouse.com/docs/get-started/sample-datasets/environmental-sensors)

insert into profile_query.sensors
SELECT *
FROM s3(
    'https://clickhouse-public-datasets.s3.eu-central-1.amazonaws.com/sensors/monthly/2019-06_bmp180.csv.zst',
    'CSVWithNames'
   )
SETTINGS format_csv_delimiter = ';';

3.  Выолняем запрос не по ключу
[1.png]
логи:
[831b49488293] 2026.09.19 14:48:06.555347 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Debug> executeQuery: (from 192.168.65.1:26161) (query 1, line 1) SELECT * FROM profile_query.sensors WHERE sensor_type = 'BMP180' settings send_logs_level = 'trace' (stage: Complete)
[831b49488293] 2026.09.19 14:48:06.556097 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Trace> Planner: Query to stage Complete
[831b49488293] 2026.09.19 14:48:06.556294 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Debug> MemoryTrackerUtils: Lower number of threads for query to 5 (10 requested)
[831b49488293] 2026.09.19 14:48:06.556506 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Trace> Planner: Query from stage FetchColumns to stage Complete
[831b49488293] 2026.09.19 14:48:06.557153 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Debug> MemoryTrackerUtils: Lower number of threads for query to 5 (10 requested)
[831b49488293] 2026.09.19 14:48:06.557808 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Trace> QueryPlanOptimizePrewhere: The min valid primary key position for moving to the tail of PREWHERE is -1
[831b49488293] 2026.09.19 14:48:06.557835 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Trace> QueryPlanOptimizePrewhere: Moved 1 conditions to PREWHERE
[831b49488293] 2026.09.19 14:48:06.557992 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Key condition: unknown
[831b49488293] 2026.09.19 14:48:06.558074 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Query condition cache has dropped 0/250 granules for PREWHERE condition equals(__table1.sensor_type, 'BMP180'_String).
[831b49488293] 2026.09.19 14:48:06.558101 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Query condition cache has dropped 0/250 granules for WHERE condition equals(sensor_type, 'BMP180'_String).
[831b49488293] 2026.09.19 14:48:06.558111 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Trace> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Filtering marks by primary and secondary keys
[831b49488293] 2026.09.19 14:48:06.558409 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): PK index has dropped 0/250 granules, it took 0ms across 2 threads.
[831b49488293] 2026.09.19 14:48:06.558466 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Selected 2/2 parts by partition key, 2 parts by primary key, 250/250 marks by primary key, 250 marks to read from 2 ranges
[831b49488293] 2026.09.19 14:48:06.558505 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Trace> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Spreading mark ranges among streams (default reading)
[831b49488293] 2026.09.19 14:48:06.558719 [ 775 ] {259fbfe6-cf5c-4237-9fb9-a9be4ce852cb} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Reading approx. 2040737 rows with 5 streams

EXPLAIN запроса [2.png]
видим что в строке P

4. выполним запрос по ключу [3.png]
Логи:
831b49488293] 2026.09.19 14:57:30.678293 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Debug> executeQuery: (from 192.168.65.1:26161) (query 1, line 1) SELECT * FROM profile_query.sensors WHERE timestamp>'2019-06-01 00:11:14' and sensor_id=15144 SETTINGS send_logs_level = 'trace' (stage: Complete)
[831b49488293] 2026.09.19 14:57:30.679245 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Trace> Planner: Query to stage Complete
[831b49488293] 2026.09.19 14:57:30.679438 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Debug> MemoryTrackerUtils: Lower number of threads for query to 5 (10 requested)
[831b49488293] 2026.09.19 14:57:30.679613 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Trace> Planner: Query from stage FetchColumns to stage Complete
[831b49488293] 2026.09.19 14:57:30.680063 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Debug> MemoryTrackerUtils: Lower number of threads for query to 5 (10 requested)
[831b49488293] 2026.09.19 14:57:30.680742 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc): Loading statistics
[831b49488293] 2026.09.19 14:57:30.680850 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Trace> QueryPlanOptimizePrewhere: The min valid primary key position for moving to the tail of PREWHERE is 1
[831b49488293] 2026.09.19 14:57:30.680886 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Trace> QueryPlanOptimizePrewhere: Moved 2 conditions to PREWHERE
[831b49488293] 2026.09.19 14:57:30.681077 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Key condition: (column 0 in [1559347875, +Inf)), (column 1 in [15144, 15144]), and
[831b49488293] 2026.09.19 14:57:30.681190 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Query condition cache has dropped 5/250 granules for PREWHERE condition and(equals(__table1.sensor_id, 15144_UInt16), greater(__table1.timestamp, '2019-06-01 00:11:14'_String)).
[831b49488293] 2026.09.19 14:57:30.681220 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Query condition cache has dropped 0/245 granules for WHERE condition and(greater(timestamp, '2019-06-01 00:11:14'_String), equals(sensor_id, 15144_UInt16)).
[831b49488293] 2026.09.19 14:57:30.681227 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Trace> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Filtering marks by primary and secondary keys
[831b49488293] 2026.09.19 14:57:30.681460 [ 816 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Trace> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Used generic exclusion search over index for part all_2_2_0 with 171 steps
[831b49488293] 2026.09.19 14:57:30.681474 [ 829 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Trace> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Used generic exclusion search over index for part all_1_1_0 with 186 steps
[831b49488293] 2026.09.19 14:57:30.681642 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): PK index has dropped 0/245 granules, it took 0ms across 2 threads.
[831b49488293] 2026.09.19 14:57:30.681708 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Selected 2/2 parts by partition key, 2 parts by primary key, 245/250 marks by primary key, 245 marks to read from 4 ranges
[831b49488293] 2026.09.19 14:57:30.681739 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Trace> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Spreading mark ranges among streams (default reading)
[831b49488293] 2026.09.19 14:57:30.681981 [ 775 ] {34a3f5df-d933-4ee7-9396-50b45ea8730a} <Debug> profile_query.sensors (129451c8-8879-4b32-baf7-554be1cfc4bc) (SelectExecutor): Reading approx. 1999777 rows with 5 streams

EXPLAIN этого запроса

И по логам и по плану заппроса видна разница.
"Selected 2/2 parts by partition key, 2 parts by primary key, 245/250 marks by primary key, 245 marks to read from 4 ranges"  - c primary key

"Selected 2/2 parts by partition key, 2 parts by primary key, 250/250 marks by primary key, 250 marks to read from 2 ranges" - без primary key

 В explain в первом случае строка primary key не заполнена , во втором случае
 выделены колонки которые включены в primary key