from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from dateutil.parser import parse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ycw625!!'
client = MongoClient('localhost', 27017)
user_db = client['user']
image_belt_db = client['image_belt']


def get_belts_data(user):
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


@app.route('/', methods=['GET', 'POST'])
def home():
    users = user_db.users
    logged_in_user = users.find_one({'login_state': True})

    if logged_in_user:
        belts_data = get_belts_data(logged_in_user)
        return render_template('home.html', login_state=True, login_time=logged_in_user['login_time'], username=logged_in_user['username'], belts=belts_data)

    if request.method == 'POST':
        attempting_user = users.find_one({'username': request.form['username']})

        if attempting_user and check_password_hash(attempting_user['password'], request.form['password']):
            current_time = datetime.now().strftime('%m/%d %H:%M login')
            users.update_one({'username': request.form['username']}, {"$set": {'login_state': True, 'login_time': current_time}})
            belts_data = get_belts_data(attempting_user)
            return render_template('home.html', login_state=True, login_time=current_time, username=request.form['username'], belts=belts_data)

        flash('아이디 또는 비밀번호가 일치하지 않습니다.')

    return render_template('home.html', login_state=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = user_db.users
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['password_check']
        belt_num = int(request.form['belt_num'])

        if users.find_one({'username': username}):
            flash('이미 사용중인 아이디 입니다.')
        elif password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.')
        else:
            hashed_password = generate_password_hash(password)
            users.insert_one({'username': username, 'password': hashed_password, 'login_state': False, 'belt_num': belt_num})

            for i in range(1, belt_num + 1):
                belt_collection = image_belt_db[f"belt{i}"]
                belt_collection.insert_one({'username': username})
            return redirect(url_for('home'))

        return render_template('register.html', username=username)

    return render_template('register.html')


@app.route('/logout')
def logout():
    users = user_db.users
    users.update_one({'login_state': True}, {"$set": {'login_state': False}})
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)