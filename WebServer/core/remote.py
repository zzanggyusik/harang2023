from flask import Blueprint, render_template, session, redirect, url_for, flash
from .db_manager import DBManager
from .instance.db_config import *
from .instance.config import *
from dateutil.parser import parse
import datetime
from .XrayController import XrayController
import zmq

remote = Blueprint("remote", __name__, url_prefix="/remote")

db_manager = DBManager()
xray_config = XrayConfig()

context = zmq.Context()
dealer = context.socket(zmq.DEALER)
dealer.connect(f'tcp://{xray_config.host}:{xray_config.port}')


@remote.route('/', methods=['GET'])
def show_remote():
    # 로그인 되어 있는지 확인
    if "user_id" not in session:
        return redirect(url_for('login.login_user'))    
    # 사용자가 소유한 벨트 데이터 조회
    belts_data = db_manager.get_user_recent_belts_image(session["user_id"])
    
    for database, value in belts_data.items():
        config = db_manager.read(db= database, collection=Collection.Config)
        
        if belts_data[database]:
            belts_data[database]["running_state"] = config["running_state"]
            belts_data[database]["belt_name"] = config["belt_name"]
    print(belts_data)
    
    return render_template('remote.html', belts_data= belts_data)

@remote.route('/detail/<belt_id>', methods=['GET'])
def belt_detail(belt_id):
    # 로그인 되어 있는지 확인
    if "user_id" not in session:
        return redirect(url_for('login.login_user'))    
    
    if '"' in belt_id:
        pass
    
    else:
        belt_config = db_manager.read(db= belt_id, collection= Collection.Config)
        
        if not belt_config:
            return "Belt not found!", 404        
        
        recent_belt_log = db_manager.get_user_recent_belt_log(belt_id)
        
        recent_belt_document = db_manager.mongo_client[belt_id][recent_belt_log].find_one(sort= [("time_uploaded", -1)])
        
        time_now = datetime.datetime.now().strftime('%Y-%m-%d/%H:%M:%S')
        
        
        return render_template('remote_detail.html',
                            belt_id= belt_id,
                            belt_config= belt_config,
                            recent_belt_document= recent_belt_document,
                            time_now = time_now)

@remote.route('/detail/<belt_id>/start', methods=['GET'])
def remote_start(belt_id):
    # 로그인 되어 있는지 확인
    if "user_id" not in session:
        return redirect(url_for('login.login_user'))  
    
    result = dealer.send_string(xray_config.message)
    
    
    if result:
        flash("Start Success!")
    else:
        flash("Start Fail!")
    
    return redirect(url_for('remote.belt_detail', belt_id= belt_id))
    
@remote.route('/detail/<belt_id>/stop', methods=['GET'])
def remote_stop(belt_id):    
    # 로그인 되어 있는지 확인
    if "user_id" not in session:
        return redirect(url_for('login.login_user'))  
    
    return "Stop!"    
        


def get_remote_blueprint():
    return remote