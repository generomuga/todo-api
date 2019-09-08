from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

#Configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root@localhost'
app.config['MYSQL_DATABASE_DB'] = 'todo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)