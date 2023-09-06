from flask import Blueprint, Flask, render_template, request, jsonify, redirect, url_for, flash, get_flashed_messages
from .db_manager import DBManager
from .instance.db_config import *
from werkzeug.security import generate_password_hash
import datetime

register = Blueprint("register", __name__, url_prefix="/register")

db_manager = DBManager()

@register.route('/', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        password_check = request.form['password_check']
        
        belt_name_list = request.form.getlist("belt_name[]")
        belt_type_list = request.form.getlist("belt_type[]")
        belt_ip_list = request.form.getlist("belt_ip[]")
        belt_port_list = request.form.getlist("belt_port[]")
        
        if password != password_check:
            # 비밀번호와 확인이 일치하지 않을 때
            flash("패스워드가 일치하지 않습니다! 다시 한번 입력해주세요.")
            return render_template('register.html')

        if db_manager.read(db= Database.Users, collection= Collection.User, key= Key.user_id, value= user_id):
            # 이미 존재하는 아이디일 경우
            flash("user_id already exists")
            return render_template('register.html')

        password_hash = generate_password_hash(password)
        user_data = {
            'user_id': user_id,
            'password': password_hash,  # 해싱된 비밀번호 저장
            'belts': belt_name_list
        }
        
        db_manager.create(db= Database.Users, collection= Collection.User, value= user_data)

        # 사용자가 선택한 각 벨트에 대해 Belt Document 생성
        for index, value in enumerate(belt_name_list):
            
            value = {
                "user_id": user_id,
                "belt_name": belt_name_list[index],
                "belt_type": belt_type_list[index],
                "belt_ip": belt_ip_list[index],
                "belt_port": int(belt_port_list[index]),
                "created_date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "running_state": False
            }
            
            create = db_manager.create(db= Database.user_conveyorbelt(user_id, belt_name_list[index]),\
                collection= Collection.Config, value= value)
            
            # result = db_manager.create_belt(belt_data)
            
            # if "error" in create:
            #     flash(create["error"])
            #     return render_template('register.html')
        
        # 성공적으로 등록된 경우 리다이렉트
        return redirect(url_for('login.login_user'))

@register.route('/check_id', methods=['POST'])
def check_id():
    user_id = request.form['id']
    if db_manager.read(db= Database.Users, collection= Collection.User, key= Key.user_id, value= user_id):
        return jsonify({'msg': '이미 존재하는 아이디 입니다.'})
    else:
        return jsonify({'msg': '사용할 수 있는 아이디 입니다.'})
    
def get_register_blueprint():
    return register