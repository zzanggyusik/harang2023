from flask import Blueprint, Flask, render_template, request, jsonify, redirect, url_for
from .db_manager import DBManager
from werkzeug.security import generate_password_hash
from flask import flash, get_flashed_messages

register = Blueprint("register", __name__, url_prefix="/register")

db_manager = DBManager()

@register.route('/', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_check = request.form['password_check']
        
        if password != password_check:
            # 비밀번호와 확인이 일치하지 않을 때
            flash("Password and password check do not match")
            return render_template('register.html')

        if db_manager.find_user_by_username(username):
            # 이미 존재하는 아이디일 경우
            flash("Username already exists")
            return render_template('register.html')

        password_hash = generate_password_hash(password)
        user_data = {
            'username': username,
            'password': password_hash,  # 해싱된 비밀번호 저장
            'belts': request.form.getlist('belt[]')
        }
        
        inserted_user = db_manager.create_user(user_data)

        # 사용자가 선택한 각 벨트에 대해 Belt Document 생성
        for belt_name in user_data['belts']:
            belt_data = {
                'belt_name': belt_name,
                'user_id': inserted_user.inserted_id
            }
            result = db_manager.create_belt(belt_data)
            if "error" in result:
                flash(result["error"])
                return render_template('register.html')
        
        # 성공적으로 등록된 경우 리다이렉트
        return redirect(url_for('login.login_user'))

@register.route('/check_id', methods=['POST'])
def check_id():
    username = request.form['id']
    if db_manager.find_user_by_username(username):
        return jsonify({'msg': '이미 존재하는 아이디 입니다.'})
    else:
        return jsonify({'msg': '사용할 수 있는 아이디 입니다.'})
    
def get_register_blueprint():
    return register