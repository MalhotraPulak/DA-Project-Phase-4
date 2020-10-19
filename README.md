### TEAM SATURN
- Ashwin Rao 2019101050
- Pulak Malhotra 2019101049
- Vishal Reddy Mandadi 2019101119

#### File Structure
- README.md (this file)
- bloodbank.sql contains the code for generating the database and adding some sample data to it
- bloodbank.py has the python code which provides an interface to access the database
- commands.sql contains the commands which are implemented in bloodbank.py but in plain SQL format (do not run them directly as they are just for syntax and all the forgein key constraints have not been satisfied for the insert commands) 




####Prerequisites
1. Python3 installed on the system, ```python3``` or ```python``` from terminal should invoke the python3 interpreter
2. MySQL server and CLI installed. ```mysql``` from terminal should point to the mysql CLI binary
3. Access to mysql account which has permission to create and use a database
4. To download pymsql, prettytable package run the following command
```pip3 install prettytable pymysql``` or ```pip install prettytable pymysql```

####How to Run
1. Start MySQL server on your machine, for ubuntu this is ```sudo /etc/init.d/mysql start```
2. Make sure you know the credentials of an account which has privilege to create a new database and access it and also Prettytable and PyMySQL package is installed in the currently active python environment
3. Change into the directory in which this README.md is present
4. Run command 
```
mysql -u <username> -p 
``` 
5. Enter password and then run the following command inside mysql CLI
```
source bloodbank.sql
```
6. All queries should run without any errors. Press CTRL-D to exit the MySQL CLI
7.  Run 
```
python3 bloodbank.py
``` from the same directory as this README
8. It will prompt you for username and password once again. On entering that it will show you the available queries.


