1. create database restaruant -- создание БД
2. create table restaruant.menu
    (
    name String comment 'Название блюда',

    weight UInt16 comment 'Вес блюда',

    weight_meet Nullable(UInt16) comment 'Вес мяса в блюде',

    author LowCardinality(String) comment 'автор блюда',

    `date` Date,

    DateTime_Insert Datetime Default now()
    )
    engine = MergeTree
3. INSERT: 
        INSERT INTO restaruant.menu
        (name, weight, weight_meet, author, `date`)
        VALUES('cesar', 320, 90, 'chef', today())
    UPDATE:
        ALTER TABLE restaruant.menu 
        UPDATE weight_meet=110
        where name='cesar'
    DELETE:
        ALTER TABLE restaruant.menu DELETE 
        WHERE author='suchef'
4. Добавляем поле в таблицу:
        ALTER TABLE restaruant.menu add column Remark Nullable(String)
    Удаляем существующее поле:
        ALTER TABLE restaruant.menu drop column Remark 
5. Создаем тестовую таблицу:

REATE TABLE nyc_taxi.trips_small_test
(

    `trip_id` UInt32,

    `pickup_datetime` DateTime,

    `dropoff_datetime` DateTime,

    `pickup_longitude` Nullable(Float64),

    `pickup_latitude` Nullable(Float64),

    `dropoff_longitude` Nullable(Float64),

    `dropoff_latitude` Nullable(Float64),

    `passenger_count` UInt8,

    `trip_distance` Float32,

    `fare_amount` Float32,

    `extra` Float32,

    `tip_amount` Float32,

    `tolls_amount` Float32,

    `total_amount` Float32,

    `payment_type` Enum8('CSH' = 1,
 'CRE' = 2,
 'NOC' = 3,
 'DIS' = 4,
 'UNK' = 5),

    `pickup_ntaname` LowCardinality(String),

    `dropoff_ntaname` LowCardinality(String)
)
ENGINE = MergeTree
PRIMARY KEY (pickup_datetime,
 dropoff_datetime)
ORDER BY (pickup_datetime,
 dropoff_datetime)
partition by toYYYYMMDD(pickup_datetime)
SETTINGS index_granularity = 8192;


Выбираем данные из источника на S3:

SELECT
    trip_id,
    pickup_datetime,
    dropoff_datetime,
    pickup_longitude,
    pickup_latitude,
    dropoff_longitude,
    dropoff_latitude,
    passenger_count,
    trip_distance,
    fare_amount,
    extra,
    tip_amount,
    tolls_amount,
    total_amount,
    payment_type,
    pickup_ntaname,
    dropoff_ntaname
FROM s3(
    'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_{0..2}.gz',
    'TabSeparatedWithNames'
) limit 100

Переливаем данные в созданную таблицу из источника:
INSERT INTO nyc_taxi.trips_small_test 
SELECT
    trip_id,
    pickup_datetime,
    dropoff_datetime,
    pickup_longitude,
    pickup_latitude,
    dropoff_longitude,
    dropoff_latitude,
    passenger_count,
    trip_distance,
    fare_amount,
    extra,
    tip_amount,
    tolls_amount,
    total_amount,
    payment_type,
    pickup_ntaname,
    dropoff_ntaname
FROM s3(
    'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_{0..2}.gz',
    'TabSeparatedWithNames'
);

Получаем список партиций в таблице:

SELECT  *
FROM system.parts
WHERE database = 'nyc_taxi'
  AND table = 'trips_small_test'
  AND active = 1
ORDER BY partition;

DETACH:
        ALTER TABLE nyc_taxi.trips_small_test DETACH PARTITION 20150701;
ATTACH:
        ALTER TABLE nyc_taxi.trips_small_test ATTACH PARTITION 20150701;
DROP: 
        ALTER TABLE nyc_taxi.trips_small_test  drop  PARTITION 20150702;
Добавление данных партициями:
        ALTER TABLE nyc_taxi.trips_small_test  ATTACH PARTITION 20150701 FROM nyc_taxi.trips_small_test

