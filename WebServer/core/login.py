from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .db_manager import DBManager
from .instance.db_config import *
from werkzeug.security import check_password_hash
import datetime
from markupsafe import escape


login = Blueprint("login", __name__)

db_manager = DBManager()

@login.route('/', methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        # 사용자가 로그인되어 있다면
        if "user_id" in session:
            print(f"로그인 - {session['user_id']}")
            
            # 사용자의 벨트 이미지 불러옴
            # belts_data = db_manager.get_belts_image_data(user_id)
            # 메인 홈페이지 표시
            return render_template('main_login.html', belts=belts_data) % escape(session["user_id"])
        
        # 로그인 페이지 렌더링
        print("로그인되어 있지 않습니다!")
        return render_template('main_unlogin.html')

    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        
        user = db_manager.read(db= Database.Users, collection= Collection.User, key= "user_id", value= user_id)
        # 사용자가 존재하지 않거나 비밀번호가 일치하지 않는 경우
        if user is None or not check_password_hash(user['password'], password):
            flash("아이디가 존재하지 않거나 비밀번호가 일치하지 않습니다.")
            return render_template('main_unlogin.html')

        if user is not None and check_password_hash(user['password'], password):
            # 로그인 상태 및 시간 업데이트
            login_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db_manager.update(db= Database.Users, collection= Collection.User,\
                key_where= "user_id", value_where= user["user_id"],\
                    key_set= "login_time", value_set= login_time)

            # 사용자 ID를 세션에 저장
            session["user_id"] = user_id
            
            databases = [db for db in db_manager.read(mode= Mode.ALL_DATABASES) if user_id in db]
            
            get_belts_image(user_id, databases)
            
            # 로그인 성공, 홈 페이지로 리디렉트
            return render_template('main_login.html', login_time=login_time, belts=belts_data)

@login.route('/logout')
def logout_user():
    session.pop('user_id', None)  # 사용자 ID를 세션에서 제거
    return redirect(url_for('login.login_user'))  # 로그인 페이지로 리디렉트

def get_login_blueprint():
    return login

def get_belts_image(user_id, databases):
    
    for index, value in enumerate(databases):
        # 가장 최신 Collection return
        recent_collection = \
            sorted(db_manager.mongo_client[value].list_collection_names(), reverse= True)
            
        print(f"recent_collection = {recent_collection}")
            
    # user_conveyorbelt = db_manager.read(db= user_conveyorbelt(user_id, databases), collection= Collection.User,\
    #     key = "user_id", value= session["user_id"])
    
    # print(user_conveyorbelt)