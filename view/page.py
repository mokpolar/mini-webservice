from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for
from control.user_mgmt import User
from flask_login import login_user

# redirect : return을 다른 라우팅 경로로 변경해줌
# url_for : routing 시 Blueprint 이n  름을 사용. 

page_abtest = Blueprint('page', __name__)

@page_abtest.route('/main')
def main():
    return render_template('page_a.html')


@page_abtest.route('/set_email', methods = ['GET', 'POST'])
def set_email():
    if request.method == 'GET':
        print('set_email', request.args.get('user_email'))
        return redirect(url_for('page.main')) # blueprint_name.function_name
    else:
        print('set_email', request.headers)

        # content type 이 application/json 인 경우, 현재는 form으로 전달되어 있기 때문에 content type이  application/x-www-form-urlencoded 으로 출력
        #print('set_email', request.get_json())
        print('set_email', request.form['user_email'])

        # user 생성.
        user = User.create(request.form['user_email'], 'A')

        # 이후 session 정보가 필요함
        login_

        return redirect(url_for('page.main'))
    #return redirect('/page/main')
    # return make_response(jsonify(success = True), 200)