from flask import Blueprint, render_template, session, redirect, url_for
from .db_manager import DBManager

remote = Blueprint("remote", __name__, url_prefix="/remote")

db_manager = DBManager()

@remote.route('/', methods=['GET'])
def show_remote():
    # 로그인 되어 있는지 확인
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login.login_user'))

    # 사용자가 소유한 벨트 데이터 조회
    belts_data = db_manager.get_belts_data(user_id)

    # 필요한 데이터 형식으로 가공
    belts_info = []
    for belt_data in belts_data:
        belt_info = db_manager.find_belt_by_id(belt_data['belt_id'])
        belts_info.append({
            'image_path': belt_data['image_path'],  # 가장 최근 이미지
            'name': belt_info['name'], # 벨트 이름
            'kind': belt_info['kind'], # figma에서 kind
            'status': belt_info['status'] # 벨트 작동상태(빨강, 초록)
        })

    return render_template('remote.html', belts=belts_info)


@remote.route('/detail', methods=['GET'])
def show_remote_detail(username, belt_id):
    # 로그인 되어 있는지 확인
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login.login_user'))

    # 벨트 정보 조회
    belt = db_manager.find_belt_by_id(belt_id)
    if not belt:
        return "Belt not found", 404

    belt_info = {
        'image_path': belt['images'][0]['image_path'],  # 가장 최근 이미지
        'ipcam_url': belt['ipcam_url'], # 실시간 ipcam의 url
        'name': belt['name'], # 벨트의 이름
        'kind': belt['kind'], # figma에서 kind
        'detection': belt['detection'], # 이상 감지
        'status': belt['status'] # 벨트 작동상태(start, stop)
    }

    return render_template('remote_detail.html', belt=belt_info)

def get_remote_blueprint():
    return remote