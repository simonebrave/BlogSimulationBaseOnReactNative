USERNAME = 'simone'
PASSWORD = 'simone'
IP = '192.168.10.109'
PORT = '3306'
DATABASE = 'blog'
PARAMS = 'charset=utf8mb4'

URL = "mysql+pymysql://{}:{}@{}:{}/{}?{}".format(USERNAME, PASSWORD, IP, PORT, DATABASE, PARAMS)

DATABASE_DEBUG = True

WSIP = '127.0.0.1'
WSPORT = 9000

AUTH_SECRET = "@hello@secure@"
AUTH_EXPIRE = 8*60*60








