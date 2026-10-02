1.  Запустил локально в контейнере Kafka c UI [1.png]
2. Создаем таблицу с Движком Kafka на основе таблицы products из предыдущего ДЗ по airbyte:
CREATE TABLE kafka_stream_table_out
(
     `make` Nullable(String),
    `year` Nullable(Int64),
    `model` Nullable(String),
    `price` Nullable(Decimal(38, 9)),
    `created_at` Nullable(DateTime64(3)),
    `updated_at` DateTime64(3)
)
ENGINE = Kafka
SETTINGS 
    kafka_broker_list = 'host.docker.internal:9092',
    kafka_topic_list = 'my_clickhouse_topic',
    kafka_group_name = 'clickhouse_consumers',
    kafka_format = 'JSONEachRow';

2.  Передадим данные в Каfka с помощью INSERT в таблицу:
INSERT INTO "airbyte_test"."kafka_stream_table_out"
SELECT  `make`,
    `year` ,
    `model` ,
    `price` ,
    `created_at` ,
    `updated_at` 
 FROM airbyte_test.products
 [3.png]

 Все данные попали в топик [4.png]

 4. Теперь прочитаем данные из топика по средствам MV:
 Создадим таблицу такую же как products
 CREATE TABLE airbyte_test.data_from_kafka as airbyte_test.products
 [5.png]
 Создадим MV:
 CREATE MATERIALIZED VIEW airbyte_test.kafka_to_clickhouse_mv TO airbyte_test.data_from_kafka AS
SELECT  `make`,
    `year` ,
    `model` ,
    `price` ,
    `created_at` ,
    `updated_at` 
 FROM airbyte_test.kafka_stream_table_out
 [6.png]

 5. Данные из итоговой таблицы [7.png]

 P.S. Попадает одна последняя строка потому что пишем и читаем через одну таблицу с движком Kafka (что на практике естественно недопустимо)