1.
CREATE TABLE default.covid19 on cluster cluster_1S_2R
(

    `date` Date,

    `location_key` LowCardinality(String),

    `new_confirmed` Int32,

    `new_deceased` Int32,

    `new_recovered` Int32,

    `new_tested` Int32,

    `cumulative_confirmed` Int32,

    `cumulative_deceased` Int32,

    `cumulative_recovered` Int32,

    `cumulative_tested` Int32
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/{uuid}/covid19',
 '{replica}')
ORDER BY (location_key,
 date)
SETTINGS index_granularity = 8192;

[1.png]

2. 
SELECT
getMacro(‘replica’),
*
FROM remote(’разделенный запятыми список реплик’,system.parts)
FORMAT JSONEachRow; 
[2.png], [2.json]

SELECT * FROM system.replicas FORMAT JSONEachRow;

[3.png], [3.json]

3. 
ALTER TABLE `default`.covid19
MODIFY TTL `date` + INTERVAL 7 DAY;

[4.png]
