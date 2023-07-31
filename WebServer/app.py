from flask import Flask, redirect, request, url_for, render_template, jsonify, session
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'secret key'
client = MongoClient('localhost', 27017)
db = client.harang

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'user' in session and 'image' in request.files:
        user = session['user']
        file = request.files['image']
        belt = request.form['belt']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image = {'belt_id': belt, 'url': url_for('static', filename='uploads/' + filename), 'timestamp': datetime.utcnow()}
            db.ConveyorBelt.insert_one(image)

            return redirect(url_for('main_login'))
    
    return redirect(url_for('main_unlogin'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' in session and session['user']['login_state']:  
        return redirect(url_for('main_login')) 
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
            session['user'] = user  
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
    if 'user' in session:  
        user = session['user']
        belts = user['belts']
        belt_images = {}
        for belt in belts:
            image = db.ConveyorBelt.find_one({'belt_id': belt}, sort=[('timestamp', -1)])
            if image:
                belt_images[belt] = image['url'] 
            else:
                belt_images[belt] = 'No image'
        return render_template('main_login.html', user=user, belt_images=belt_images)
    return redirect(url_for('main_unlogin'))

@app.route('/logout')
def logout():
    user_id = session['user']['_id']
    db.User.update_one({'_id': user_id}, {'$set': {'login_state': False}})  
    session.pop('user', None)  
    return redirect(url_for('main_unlogin'))  

@app.route('/upload', methods=['GET'])
def upload():
    if 'user' in session:  
        user = session['user']
        return render_template('upload.html', user=user)
    return redirect(url_for('main_unlogin'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)