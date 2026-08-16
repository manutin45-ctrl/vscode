1.  create table sale.sales
    (
    id UInt32,
    product_id UInt32,
    quantity UInt32,
    price Float32,
    sale_date DateTime default now()
    )
    engine = MergeTree()
    order by (id);
    [1.png]

2.  
    alter table sale.sales add projection sales_projection
    (
    select
	    product_id,
	    sum(quantity * price)
    group by
	    product_id
    )
    [2.png]
3.  create table sale.sum_sales
	(
	product_id UInt32,
	total_quantity UInt32,
	total_sales Float32
	)
    engine=SummingMergeTree()
    order by product_id

    create materialized view sales_mv to sale.sum_sales
    AS
    select product_id, sum(quantity) as total_quantity , sum (quantity * price) as total_sales
    from sale.sales 
    group by product_id
    [3.png]
4.  Запрос из проекции
    [4.png]
5.  Запрос из mat view 
    [5.png]
6. Запрос к таблице с запретом на использование проекции
    [6.png]

Вывод: запросы к проекции и mat view выполняются на поряок быстрее, так как данные уже 
предрасчитаны.