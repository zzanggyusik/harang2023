from flask import Blueprint, render_template, session, redirect, url_for
from .db_manager import DBManager
from .instance.db_config import *
from dateutil.parser import parse

remote = Blueprint("remote", __name__, url_prefix="/remote")

db_manager = DBManager()

@remote.route('/', methods=['GET'])
def show_remote():
    # 로그인 되어 있는지 확인
    if "user_id" not in session:
        return redirect(url_for('login.login_user'))

    # 사용자가 소유한 벨트 데이터 조회
    belts_data = db_manager.get_user_recent_belts_image(session["user_id"])
    print(belts_data)
    
    for database, value in belts_data.items():
        config = db_manager.read(db= database, collection=Collection.Config)
        print(config["running_state"])
        if belts_data[database]:
            belts_data[database]["running_state"] = config["running_state"]
            belts_data[database]["belt_name"] = config["belt_name"]
    
    return render_template('remote.html', belts_data= belts_data)

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