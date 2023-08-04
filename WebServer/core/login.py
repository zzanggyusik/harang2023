# Example
# TODO 
# 로그인 기능을 모듈화
from flask import Blueprint, render_template, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from .instance.config import *
from pymongo import MongoClient
from dateutil.parser import parse

# Login 블루프린트 지정
login = Blueprint("login", __name__)
## 아래처럼 url_prefix로 url을 지정할 수 있음
# http://localhost:5000/login/~
# login = Blueprint("login", __name__, url_prefix="/login")

# MongoDB 초기화
client = MongoClient(MONGODB_IP, MONGODB_PORT)
user_db = client['user']
image_belt_db = client['image_belt']

@login.route('/', methods=['GET', 'POST'])
def home():
    users = user_db.users
    
    # DB에 login_state가 True인 사용자가 여러명이면 어쩌지?
    logged_in_user = users.find_one({'login_state': True})

    # 로그인 되어있는 사용자면
    if logged_in_user:
        # 사용자의 벨트 이미지 불러옴
        belts_data = get_belts_data(logged_in_user)
        
        # 메인 홈페이지 표시
        return render_template('home.html', login_state=True, \
                                login_time=logged_in_user['login_time'], username=logged_in_user['username'], \
                                belts=belts_data)

    # / 페이지로부터 POST 요청 시
    if request.method == 'POST':
        # / 페이지로부터 받은 username을 DB에서 조회
        attempting_user = users.find_one({'username': request.form['username']})
        
        # DB에 사용자 정보가 있고 비밀번호가 일치한다면
        if attempting_user and check_password_hash(attempting_user['password'], request.form['password']):
            # 현재 시간 표시
            current_time = datetime.now().strftime('%m/%d %H:%M login')
            
            # {Username} 정보 업데이트
            users.update_one({'username': request.form['username']}, {"$set": {'login_state': True, 'login_time': current_time}})
            
            # 현재 연결을 시도한 사용자의 벨트 이미지를 불러옴
            belts_data = get_belts_data(attempting_user)
            return render_template('home.html', login_state=True, \
                                    login_time=current_time, username=request.form['username'], \
                                    belts=belts_data)

        flash('아이디 또는 비밀번호가 일치하지 않습니다.')

    # 로그인 실패
    return render_template('home.html', login_state=False)

def get_belts_data(user) -> list:
    """MongoDB로부터 사용자의 벨트별 이미지를 불러오는 함수

    Args:
        user (string): DB에 저장된 유저 ID

    Returns:
        list: 벨트 이미지
    """
    belts_data = []
    for i in range(1, user['belt_num'] + 1):
        belt_coll = image_belt_db[f"belt{i}"]
        belt_doc = belt_coll.find_one({'username': user['username']})
        if belt_doc is not None:
            belt_doc['images'].sort(key=lambda x: parse(x['time_uploaded']), reverse=True)
            belts_data.append({
                'belt_id': i,
                'image_path': belt_doc['images'][0]['image_path']
            })
    return belts_data