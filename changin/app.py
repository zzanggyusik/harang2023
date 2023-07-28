from flask import Flask, redirect, request, url_for, render_template, jsonify, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret key'
client = MongoClient('localhost', 27017)
db = client.harang

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('main_unlogin'))


@app.route('/main_unlogin', methods=['GET', 'POST'])
def main_unlogin():
    if request.method == 'POST':
        user_id = request.form.get('id')
        password = request.form.get('password')
        user = db.User.find_one({'_id': user_id})
        if user and check_password_hash(user['password'], password):
            login_time = datetime.now().strftime("%Y/%m/%d %H:%M") + " login"
            db.User.update_one({'_id': user_id}, {'$set': {'login_state': True, 'last_login': login_time}})
            session['user'] = user  # 로그인한 사용자 정보를 세션에 저장합니다.
            return redirect(url_for('main_login'))
    return render_template('main_unlogin.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form.get('id')
        password = request.form.get('password')
        password_check = request.form.get('password_check')
        belts = request.form.getlist('belt[]')
        
        if password != password_check:
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        
        user = {'_id': user_id, 'password': hashed_password, 'belts': belts, 'login_state': False}
        
        db.User.insert_one(user)
        
        return redirect(url_for('main_unlogin'))
        
    return render_template('register.html')


@app.route('/check_id', methods=['POST'])
def check_id():
    user_id = request.form.get('id')
    if db.User.find_one({'_id': user_id}):
        return jsonify({'status': 'fail', 'msg': '사용할 수 없는 아이디입니다.'})
    else:
        return jsonify({'status': 'success', 'msg': '사용할 수 있는 아이디입니다.'})


@app.route('/main_login', methods=['GET', 'POST'])
def main_login():
    if 'user' in session:  # 세션에서 사용자 정보를 가져옵니다.
        user = session['user']
        belts = user['belts']
        belt_images = {}
        for belt in belts:
            image = db.ConveyorBelt.find_one({'belt_id': belt}, sort=[('timestamp', -1)])
            belt_images[belt] = image['url'] if image else 'No image'
        return render_template('main_login.html', user=user, belt_images=belt_images)
    return redirect(url_for('main_unlogin'))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)