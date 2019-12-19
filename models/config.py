DEBUG = True

HOST = '127.0.0.1'
PORT = '3306'
DATABASE_NAME = 'db_jjl'
USERNAME = 'root'
PASSWORD = 'cjjdwws144'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{databasename}?charset=utf8mb4" \
    .format(username=USERNAME, password=PASSWORD, host=HOST, port=PORT, databasename=DATABASE_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_ECHO = False
TEMPLATES_AUTO_RELOAD = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
