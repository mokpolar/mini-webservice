import pymongo

MONGO_HOST = 'localhost'
MONGO_CONN = pymongo.MongoClient('mongodb://%s' % (MONGO_HOST))

def conn_mongodb():
    try:
        MONGO_CONN.admin.command('ismaster')
        page_ab = MONGO_CONN.page_session_db.page_ab

    except:
        MONGO_CONN = pymongo.MongoClient('mongodb://%s' % (MONGO_HOST))
        page_ab = MONGO_CONN.page_session_db.page_ab
    
    return page_ab
