# rbacServer

This is a custom Role-Based Access Control (RBAC) System to manage user roles and
permissions dynamically. Have used the Django framework and its inbuilt SQL to 
implement it.


How to run 

Run Migrations
python3 manage.py makemigrations rbac_core  
python3 manage.py migrate

To run data initialization of roles and permissions

python3 manage.py create_initial_permissions 
python3 manage.py create_default_roles   

Run the Server

python3 manage.py runserver 