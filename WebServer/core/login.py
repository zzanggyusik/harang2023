from flask import Blueprint, render_template, request, redirect, url_for, session
from .db_manager import DBManager
from werkzeug.security import check_password_hash
from datetime import datetime

login = Blueprint("login", __name__)

db_manager = DBManager()

@login.route('/', methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        # 세션에서 사용자 ID를 가져옴
        user_id = session.get('user_id')

        # 사용자가 로그인되어 있다면
        if user_id:
            # 사용자의 벨트 이미지 불러옴
            belts_data = db_manager.get_belts_data(user_id)
            # 메인 홈페이지 표시
            return render_template('main.html', belts=belts_data)
        
        # 로그인 페이지 렌더링
        return render_template('home.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db_manager.find_user_by_username(username)

        # 사용자가 존재하지 않거나 비밀번호가 일치하지 않는 경우
        if user is None or not check_password_hash(user['password'], password):
            return render_template('home.html', error_message="아이디가 존재하지 않거나 비밀번호가 일치하지 않습니다.")

        if user is not None and check_password_hash(user['password'], password):
            # 로그인 상태 및 시간 업데이트
            login_time = str(datetime.utcnow())
            db_manager.update_user_login(user['_id'], login_time)

            # 사용자 고유 ID를 세션에 저장
            session['user_id'] = str(user['_id'])

            # 사용자의 벨트 이미지 불러옴
            belts_data = db_manager.get_belts_data(user['_id'])
            
            # 로그인 성공, 홈 페이지로 리다이렉트
            return render_template('main.html', login_time=login_time, belts=belts_data)

@login.route('/logout')
def logout_user():
    session.pop('user_id', None)  # 사용자 ID를 세션에서 제거
    return redirect(url_for('login.login_user'))  # 로그인 페이지로 리다이렉트

def get_login_blueprint():
    return login