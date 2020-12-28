from flask import Flask, jsonify, request, render_template, make_response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
from view import page
import os



'''
# Libraries explanation

Flaks : flask server
jsonify : REST API return as json data
request : getting arguments
render_template : return html page
make_response : status codes
LoginManager : session management
current_user : monitoring logged users
login_required : logged user only access 
login_user : login can make session
logout_user : logout
CORS : insert specific domain headers to response
'''

# https 만 지원하는 기능을 http에서 테스트할 때 필요한 설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# 서버 생성pi
app = Flask(__name__, static_url_path = '/static')

# 서버 간 REST API 지원
CORS(app) 

# 보안을 높이려면 서버를 켤 때 마다 값을 달리해야 하지만, 테스트를 위해 고정값으로
app.secure_key = 'jy_server' 

# blueprint 등록
app.register_blueprint(page.page_abtest, url_prefix='/page')

# 로그인 관리
login_manager = LoginManager()

# 로그인 매니저에 앱 등록. (플래스크 객체를)
login_manager.init_app(app)

# 세션을 보다 복잡하게 만들기
login_manager.session_protection = 'strong'

# login_manager 안에 있는 user_loader 데코레이터 사용
# id를 받아오고 mysql에서 해당 id 기반의 record를 갖고와서 이를 객체로 리턴
# 그러니까 누군가 로그인을 하면 사용자 객체를 만들어서 세션관리를 해주고 
# 새로운 요청이 왔는데 세션요청이 있으면 세션요청에서 아이드를 뽑아서 이 아이디 기반의 객체를 요청
# mysql에 저장
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# 로그인이 안 된 사용자가 로그인 사용자용 API를 리퀘스트했을 때 에러가 나면서 해당 함수 호출
# 401 : 허용이 되지 않음 http response error
@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = '8080', debug = True)




