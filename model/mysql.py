import pymysql
MYSQL_HOST = 'localhost'
MYSQL_CONN = pymysql.connect(
    host = MYSQL_HOST,
    port = 3306,
    user = 'admin',
    passwd = 'jy',
    db = 'page_db',
    charset = 'utf8' # unicode
)

def conn_mysqldb():
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect = True)
    return MYSQL_CONN