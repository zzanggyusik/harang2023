from flask import Blueprint, render_template, session, redirect, url_for
from .db_manager import DBManager
from dateutil.parser import parse

history = Blueprint("history", __name__, url_prefix="/history")

db_manager = DBManager()

@history.route('/', methods=['GET'])
def show_history():
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID를 가져옵니다.
    
    if not user_id:
        return redirect(url_for('login.login_user'))  # 만약 로그인이 되어있지 않다면 로그인 페이지로 리다이렉트합니다.
    
    belts_data = list(db_manager.find_belts_by_user_id(user_id))
    all_belts_images = []  # 모든 벨트의 이미지들을 저장할 리스트
    
    for belt_data in belts_data:
        belt = db_manager.find_belt_by_id(belt_data['belt_id'])
        user = db_manager.find_user_by_id(user_id)
        images = belt.get('images', [])
        images.sort(key=lambda x: parse(x['time_uploaded']), reverse=True)
        
        # 각 벨트에서 최근 6장의 이미지만 가져옵니다.
        recent_images = images[:6]

        all_belts_images.append({
            'username': user.get('username', 'Unknown'),
            'belt_name': belt.get('name', 'Unknown'),
            'recent_images': recent_images
        })
    
    return render_template('history.html', images=all_belts_images)

@history.route('/detail', methods=['GET'])
def show_history_detail():
    return render_template('history_detail.html')
@history.route('/detail/image', methods=['GET'])
def show_history_detail_image():
    return render_template('history_detail_image.html')

def get_history_blueprint():
    return history