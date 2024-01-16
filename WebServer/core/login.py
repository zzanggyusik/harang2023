from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .db_manager import DBManager
from .instance.db_config import *
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from markupsafe import escape


login = Blueprint("login", __name__)

db_manager = DBManager()

def week():
    today = datetime.now()

    # 현재 요일 가져오기 (0: 월요일, 1: 화요일, ..., 6: 일요일)
    current_weekday = today.weekday()

    # 현재 날짜를 기준으로 주의 시작일 계산
    start_of_week = today - timedelta(days=current_weekday)

    # 주의 종료일 계산 (7일 더하기)
    end_of_week = start_of_week + timedelta(days=6)

    # 결과를 담을 딕셔너리 초기화
    week_dict = {}
    week_data = {}
    week = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    week_1 = [1, 2, 3, 4, 3, 2, 1]
    week_2 = [3, 2, 1, 2, 3, 4, 5]
    count = 0
    
    # 주의 각 날짜와 요일을 딕셔너리에 추가
    current_date = start_of_week
    while current_date <= end_of_week:
        week_dict[current_date.strftime('%A')[:3]] = current_date.day
        
        if current_date.day == today.day:
            week_data["weekday"] = week[count]
        current_date += timedelta(days=1)
        count += 1

    # 결과 출력
    
    week_data["label"] = week
    
    week_data["var1"] = week_1
    week_data["var2"] = week_2
    
    week_data["year"] = today.year
    week_data["month"] = today.month
    week_data["day"] = today.day
    week_data["week"] = week_dict
    print(week_data)    
    
    return week_data


@login.route('/', methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        # 사용자가 로그인되어 있다면
        if "user_id" in session:
            print(f"로그인 - {session['user_id']}")
            
            # 사용자의 벨트 이미지 불러옴
            # belts_data = db_manager.get_belts_image_data(user_id)
            # 메인 홈페이지 표시
            
            # 현재 날짜와 시간 가져오기
            week_data = week()
                
            # 결과 출력
            # print(f'오늘은 {today_weekday}이고, 이번주는 {this_week_formatted[0]}부터 {this_week_formatted[-1]}까지입니다.')
            
        
            # login_time = db_manager.read(db= Database.Users, collection= Collection.User,\
            #     key= Key.user_id, value= session["user_id"])["login_time"]
            # recent_belts_info = db_manager.get_user_recent_belts_image(session["user_id"])
            
            # current_running_belts_number, all_belts_number = db_manager.get_user_running_belts(session["user_id"])
            
            # return render_template('main_login.html', recent_belts_info= recent_belts_info,\
            #     username= session['user_id'], login_time= login_time,\
            #         current_running_belts_number= current_running_belts_number, all_belts_number= all_belts_number)
            
            return render_template('main_login.html', username= session['user_id'], week_data= week_data)
        
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

        else: 
            # 로그인 상태 및 시간 업데이트
            login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db_manager.update(db= Database.Users, collection= Collection.User,\
                key_where= "user_id", value_where= user["user_id"],\
                    key_set= "login_time", value_set= login_time)

            # 사용자 ID를 세션에 저장
            session["user_id"] = user_id
            
            week_data = week()
            
            recent_belts_info = db_manager.get_user_recent_belts_image(session["user_id"])
            
            current_running_belts_number, all_belts_number = db_manager.get_user_running_belts(session["user_id"])
            
            # 로그인 성공, 홈 페이지로 리디렉트
            return render_template('main_login.html', username= session['user_id'], week_data= week_data)

@login.route('/logout')
def logout_user():
    session.pop('user_id', None)  # 사용자 ID를 세션에서 제거
    return redirect(url_for('login.login_user'))  # 로그인 페이지로 리디렉트

def get_login_blueprint():
    return login

# def check_is_login():
#     if "user_id" not in session:
#         return redirect(url_for('login.login_user'))    