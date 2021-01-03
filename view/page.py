from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for, session
from control.user_mgmt import User
from control.session_mgmt import Session
from flask_login import login_user, current_user, logout_user
import datetime

# redirect : return을 다른 라우팅 경로로 변경해줌
# url_for : routing 시 Blueprint 이n  름을 사용. 

page_abtest = Blueprint('page', __name__)

@page_abtest.route('/main')
def main():
    # 현재 로그인 된 사용자인지를 확인해야 함
    if current_user.is_authenticated:
        # 세션 정보를 갖고 와서 A B 를 번갈아가며 렌더링
        web_page_name = Session.get_page(current_user.page_id)
        # 로그인 시에 flask_login을 사용해서 사용자를 명시하는 작업이 그 전에 있어야 함
        # true 이면 로그인 된 사용자니까 
        # main_server에서 구현한 user_loader를 사용
        # 사용자 정보는 mysql db에서 갖고오는 것으로 static method로 선언한 get함수
        # 그 id를 기반으로 db에서 사용자 정보를 갖고옴
        # 그리고 그 객체는 current_user 에 자동으로 들어가게 됨
        Session.save_session_info(session['client_id'], current_user.user_email, web_page_name)

        return render_template(web_page_name, user_email = current_user.user_email)
    else:
        web_page_name = Session.get_page()
        # 현재 user_email 정보는 없는 상태로 빠지는 것이기 때문에 anonumous로 들어감. 
        Session.save_session_info(session['client_id'], 'anonymous', web_page_name)
        # 그렇지 않은 경우에는 그냥 페이지 렌더링
        # 진자에서 else 부분
        return render_template(web_page_name)


@page_abtest.route('/set_email', methods = ['GET', 'POST'])
def set_email():
    if request.method == 'GET':
        print('set_email', request.args.get('user_email'))
        return redirect(url_for('page.main')) # blueprint_name.function_name
    else:
        print('set_email', request.headers)

        # content type 이 application/json 인 경우, 현재는 form으로 전달되어 있기 때문에 content type이  application/x-www-form-urlencoded 으로 출력
        #print('set_email', request.get_json())
        #print('set_email', request.form['user_email'])

        # hidden 부분에는 page id 도 값이 들어있는데 이 부분 출력
        #print('page_id', request.form['page_id'])

        # user 생성.
        user = User.create(request.form['user_email'], request.form['page_id'])

        # flask_login 라이브러리로 사용자 세션정보를 생성해서 사용자 웹 브라우저에 같이 전송. 
        # 사용자 웹 브라우저는 이 정보를 저장하고 있다가 다시 서버에 요청시 이 쿠키정보를 포함하여 사용자를 구분할 수 있도록 함 
        # 이 세션 정보는 flask 서버 자체가 갖고 있는 기능 중 하나. flask 라이브러리에 포함된 기능임. 
        # flask login은 이 기능을 같이 쓰는 상태 
        # secret key를 기반으로 세션 정보를 생성한다 
        login_user(user, remember = True, duration = datetime.timedelta(days=365))


        return redirect(url_for('page.main'))
    #return redirect('/page/main')
    # return make_response(jsonify(success = True), 200)


@page_abtest.route('/logout')
def logout():
    # User Class 에서 현재 id라는 속성을 들고 있고 이 속성을 삭제 
    User.delete(current_user.id)
    logout_user()
    return redirect(url_for('page.main')) 
