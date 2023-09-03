from flask import Blueprint, render_template, session, redirect, url_for
from .db_manager import DBManager
from dateutil.parser import parse

remote = Blueprint("remote", __name__, url_prefix="/remote")

db_manager = DBManager()

@remote.route('/', methods=['GET'])
def show_remote():
    # 로그인 되어 있는지 확인
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login.login_user'))

    # 사용자가 소유한 벨트 데이터 조회
    belts_data = list(db_manager.find_belts_by_user_id(user_id))
    # print(f"Belts Data for user {user_id}: {belts_data}")  # 로깅

    # 필요한 데이터 형식으로 가공
    belts_info = []
    for belt_data in belts_data:
        belt_info = {
            'belt_name': belt_data.get('belt_name', 'Unknown Name'),
            'kind': belt_data.get('kind', 'Unknown Kind'),
            'status': belt_data.get('status', 'Unknown Status')
        }
        if 'images' in belt_data and belt_data['images']:
            belt_data['images'].sort(key=lambda x: parse(x['time_uploaded']), reverse=True)
            belt_info['image_path'] = belt_data['images'][0]['url']  # 'url' 필드로 접근
        else:
            belt_info['image_path'] = 'default_image_path'

        belts_info.append(belt_info)

    return render_template('remote.html', belts=belts_info)


@remote.route('/detail/<belt_name>', methods=['GET'])
def belt_detail(belt_name):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login.login_user'))

    belt_data = db_manager.find_belt_by_name_and_user_id(belt_name, user_id)

    if not belt_data:
        return "Belt not found!", 404

    if 'images' in belt_data and belt_data['images']:
        belt_data['images'].sort(key=lambda x: parse(x['time_uploaded']), reverse=True)
        image_path = belt_data['images'][0]['url']
        time_uploaded = belt_data['images'][0]['time_uploaded']
    else:
        image_path = 'default_image_path'
        time_uploaded = 'Unknown Time'

    return render_template('remote_detail.html',
                           belt=belt_data,
                           image_path=image_path,
                           belt_name=belt_data.get('belt_name'),
                           kind=belt_data.get('kind'),
                           time_uploaded=time_uploaded,
                           detection=belt_data.get('detection', 'Unknown Detection'),
                           ipcam_url=belt_data.get('ipcam_url', 'Unknown URL'))




def get_remote_blueprint():
    return remote