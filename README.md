
# FLASK BLOG
### Blog Webapp with Simple and Clean UI, using Python micro-framework Flask and MySQL database

### Initiallization steps :

Clone Git Repository

```git
git clone https://github.com/aditya1819/flaskblog.git
```
or Download from github
Use virtual env (optional)
 
Install required python libraries
```
pip install -r requirements.txt
```
Create database and required Tables from following SQL commands in 
MySQL Command line
```SQL
CREATE DATABASE flaskblog;
```
```SQL
USE flaskblog;
```
```SQL
CREATE TABLE articles (id INT(11) AUTO_INCREMENT PRIMARY KEY,title VARCHAR(255),author VARCHAR(50),body TEXT,create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
```
```SQL
CREATE TABLE users (id INT(11) AUTO_INCREMENT PRIMARY KEY,name VARCHAR(50),username VARCHAR(50),password VARCHAR(200),email VARCHAR(100),register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
```
Add MySQL Localhost Database details to `dbconnect.py` replace `user` and `passwd` by the `MySQL user` you are using or `root`
```python
class dbconnect():
    host = 'localhost'
    user = 'root'
    passwd = 'root123'
    cursorclass = 'DictCursor'
```
Run `app.py` ( Please make sure Port 5000 is available )
```python
py app.py
```
LocalHost address
```
http://127.0.0.1:5000/
or
localhost:5000
```

