from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ycw625!!'
client = MongoClient('localhost', 27017)
db = client['user_db']

@app.context_processor
def inject_title():
    return {'title': '윤채원'}

@app.route('/', methods=['GET', 'POST'])
def home():
    users = db.users
    login_user = users.find_one({'login_state': True})
    if login_user:
        return render_template('home.html', login_state=True)

    if request.method == 'POST':
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if check_password_hash(login_user['password'], request.form['password']):
                users.update_one({'username': request.form['username']}, {"$set": {'login_state': True}})
                return render_template('home.html', login_state=True)
        flash('아이디 또는 비밀번호가 일치하지 않습니다.')

    return render_template('home.html', login_state=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = db.users
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['password_check']

        if not username:
            flash('아이디를 입력하세요.')
            return render_template('register.html', username=username)
        elif not password or not confirm_password:
            flash('비밀번호를 입력하세요.')
            return render_template('register.html', username=username)

        existing_user = users.find_one({'username': username})

        if existing_user is None:
            if password == confirm_password:
                hash_pass = generate_password_hash(password)
                users.insert_one({'username': username, 'password': hash_pass, 'login_state': False})
                return redirect(url_for('home'))
            else:
                flash('비밀번호가 일치하지 않습니다.')
                return render_template('register.html', username=username)
        flash('이미 사용중인 아이디 입니다.')
        return render_template('register.html')

    return render_template('register.html')

@app.route('/logout')
def logout():
    users = db.users
    users.update_one({'login_state': True}, {"$set": {'login_state': False}})
    return render_template('home.html', login_state=False)

if __name__ == '__main__':
    app.run(port=5000, debug=True)