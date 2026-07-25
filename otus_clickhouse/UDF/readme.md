1. Общий доход всех операций:
    select sum(quantity * price) FROM `default`.transactions;
2. Средний доход с одной сделки
    select avg(quantity * price) FROM `default`.transactions;
3. Общее количество проданной продукции
    select sum(quantity) FROM `default`.transactions;
4. Количество уникальных пользователей
    select uniqExact(user_id) FROM `default`.transactions;


2.1 Преобразовать дату в строку
    select toString(transaction_date) FROM `default`.transactions;
2.2 Извлечь год и месяц
    select toString(toYYYYMM (transaction_date)) FROM `default`.transactions;
2.3 Округлить price
    select round(price) FROM `default`.transactions;
2.4 Преобразовать transaction_id в строку
    select toString(transaction_id) FROM `default`.transactions;


3.1 Функция расчета общей стоимости
    create function full_price as (price, rate) -> price * rate;
3.2 Использование созданной функции
    select *,full_price(quantity, price) FROM `default`.transactions;
3.3 Cоздание функции классификации
    create function classificator as (price) -> if(price<100, 'малоценные','высокоценные')
3.4 Вызов функции классификации
    select *,classificator( price) FROM `default`.transactions;

2 Вариант

На работе иногда используем EUDF для python скриптов (в основном для расчета сложных математических алгоритмов, которые в python довольно таки просто реализуются). Всегда реализуем это через docker контейнер. Проще с точки зрения настройки окружения и установки нужных зависимостей. И нет влияния одних eudf функций на другие. Пример из документации:

<functions>
    <function>
        <type>executable_pool</type>
        <name>my_docker_func</name>
        <return_type>String</return_type>
        <argument>
            <type>UInt64</type>
            <name>value</name>
        </argument>
        <format>TabSeparated</format>
        <command>docker run --rm -i python:3.11 python3 /scripts/my_script.py</command>
        <execute_direct>0</execute_direct>
        <pool_size>4</pool_size>
        <max_command_execution_time>30</max_command_execution_time>
    </function>
</functions>