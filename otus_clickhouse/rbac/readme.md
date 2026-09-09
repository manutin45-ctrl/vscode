1.  CREATE USER jhon IDENTIFIED BY 'qwerty'
[1.png][2.png]
2.  CREATE ROLE devs;
[3.png][4.png]
3. GRANT SELECT ON imdb.* TO devs;
    SELECT * FROM system.grants WHERE role_name = 'devs';
[5.png][6.png]    
4.  grant devs to jhon
    SELECT granted_role_name, granted_role_is_default, with_admin_option
    FROM system.role_grants
    WHERE user_name = 'jhon';
[7.png][8.png]