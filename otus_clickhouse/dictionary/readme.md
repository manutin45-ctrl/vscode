1.  SELECT user_id, `action`, expense , dictGet( `default`.my_dict2, 'email' , user_id ) as    email 
FROM `default`.test_dict2;
[1.png]
2.  
SELECT user_id, `action`, expense , dictGet( `default`.my_dict2, 'email' , user_id ) as email,
sum(expense) OVER (
        PARTITION BY action
        ORDER BY email ASC
        
    ) AS cumulative_expense

FROM `default`.test_dict2;
[2.png]