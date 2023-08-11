from flask import Blueprint, Flask, render_template, request, jsonify, redirect, url_for
from .db_manager import DBManager
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId

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
            return jsonify({'error': "비밀번호가 일치하지 않습니다."})

        if db_manager.find_user_by_username(username):
            return jsonify({'error': "이미 존재하는 ID입니다."})

        password_hash = generate_password_hash(password)
        # 사용자 생성
        user_data = {
            'username': username,
            'password': password_hash,
        }


        # 사용자 ID 가져오기
        user_id = db_manager.create_user(user_data)

        # 사용자 ID가 ObjectId 타입인 경우 문자열로 변환
        if isinstance(user_id, ObjectId):
            user_id = str(user_id)

        # 벨트 생성
        belts = request.form.getlist('belt[]')
        for belt_name in belts:
            belt_data = {
                'user_id': user_id,
                'name': belt_name,
                'kind': '',
                'images': [],
                'ipcam_url': '',
                'detection': False,
                'status': False
            }
            db_manager.create_belt(belt_data)
        
        return redirect(url_for('login.login_user', username=username))


@register.route('/check_id', methods=['POST'])
def check_id():
    username = request.form['id']
    if db_manager.find_user_by_username(username):
        return jsonify({'msg': '이미 존재하는 아이디 입니다.'})
    else:
        return jsonify({'msg': '사용할 수 있는 아이디 입니다.'})
    
def get_register_blueprint():
    return register