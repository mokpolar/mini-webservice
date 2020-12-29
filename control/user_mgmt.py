from flask_login import UserMixin
from model.mysql import conn_mysqldb


class User(UserMixin):

    def __init__(self, user_id, user_email, page_id):
        self.id = user_id
        self.user_email = user_email 
        self.page_id = page_id

    
    def get_id(self):
        return str(self.id)


    @staticmethod
    def get(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_ID = '" + str(user_id) + "'" 
        print(sql)
        db_cursor.execute(sql)

        user = db_cursor.fetchone()
        if not user:
            return None
        
        user = User(user_id = user[0], user_email = user[1], page_id = user[2])
        return user


    @staticmethod
    def find(user_email):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_ID = '" + str(user_email) + "'" 
        print(sql)
        db_cursor.execute(sql)

        user = db_cursor.fetchone()
        if not user:
            return None
        
        user = User(user_id = user[0], user_email = user[1], page_id = user[2])
        return user

    @staticmethod
    def create(user_email, blog_id):
        user = User.find(user_email)

        if user == None:
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO user_info (USER_EMAIL, PAGE_ID) VALUES ('%s', '%s')" % (str(user_email), str(page_id)) # user_id = auto increment
            db_cursor.execute(sql)
            mysql_db.commit()
            return User.find(user_email)
        else:
            return user

