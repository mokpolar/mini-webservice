from model.mongodb import conn_mongodb
from datetime import datetime


class Session():
    page = {'A' : 'page_a.html', 'B': 'page_b.html'}
    session_count = 0


    # 접속정보를 저장
    @staticmethod
    def save_session_info(session_ip, user_email, webpage_name):
        now = datetime.now()
        now_time = now.strftime("%d/%m/%Y %H:%M:%S") # https://strftime.org/

        mongo_db = conn_mongodb()
        mongo_db.insert_one({
        'session_ip': session_ip,
        'user_email': user_email,
        'page': webpage_name,
        'access_time': now_time
        })

    
    @staticmethod
    def get_page(page_id = None):
        if page_id == None:
            if Session.session_count == 0:
                Session.session_count = 1
                return 'page_a.html'
            else:
                BlogSession.session_count = 0
                return 'page_b.html'
        else:
            return Session.page[page_id]
