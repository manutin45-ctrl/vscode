1.  CREATE TABLE tbl1
(
    UserID UInt64,
    PageViews UInt8,
    Duration UInt8,
    Sign Int8,
    Version UInt8
)
ENGINE = VersionedCollapsingMergeTree(Sign, Version)
ORDER BY UserID;
[1](1.png), [2](2.png)

2.  CREATE TABLE tbl2
(
    key UInt32,
    value UInt32
)
ENGINE = SummingMergeTree()
ORDER BY key;
[3](3.png)

3.  CREATE TABLE tbl3
(
    `id` Int32,
    `status` String,
    `price` String,
    `comment` String
)
ENGINE = ReplacingMergeTree()
PRIMARY KEY (id)
ORDER BY (id, status);

[4](4.png), [5](5.png)

4.  CREATE TABLE tbl4
(   CounterID UInt8,
    StartDate Date,
    UserID UInt64
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(StartDate) 
ORDER BY (CounterID, StartDate);



CREATE TABLE tbl5
(   CounterID UInt8,
    StartDate Date,
    UserID AggregateFunction(uniq, UInt64)
) ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(StartDate) 
ORDER BY (CounterID, StartDate);

[6](6.png), [7](7.png)

5.  CREATE TABLE tbl6
(
    `id` Int32,
    `status` String,
    `price` String,
    `comment` String,
    `sign` Int8
)
ENGINE = CollapsingMergeTree(sign)
PRIMARY KEY (id)
ORDER BY (id, status);

[9](9.png), [8](8.png)