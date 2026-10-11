1. Поднял postgre и ClicHouse в одном контейнере
2. Создал тестовую таблицу в Postgre 
[1.png]
3. Подключился через функцию в ClickHouse
[2.png]
4. Создадим таблицу с движком PostGreSQL
CREATE TABLE default.postgresql_table_test
(
   
    `id`         Int32
)
ENGINE = PostgreSQL('postgres_db:5432', 'my_database', 'pg_test_click', 'my_user', 'my_password')
[3.png], [4.png]
5. Создадим БД с движком PostGreSql
CREATE DATABASE test_database_postgre
ENGINE = PostgreSQL('postgres_db:5432', 'my_database', 'my_user', 'my_password');

и протестируем 
[5.png],[6.png]