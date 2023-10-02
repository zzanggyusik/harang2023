from flask import render_template, session, redirect, url_for, flash

from WebServer.core.remote.utils import send_numpy_data_to_main_server
from ..db_manager import DBManager
from ..instance.db_config import *
from ..instance.config import *
from dateutil.parser import parse
import datetime
from ..XrayController import XrayController
import zmq
import requests
from PIL import Image
import numpy as np
import io
import base64
# from config import MainServerConfig

db_manager = DBManager()
xray_config = XrayConfig()

context = zmq.Context()
dealer = context.socket(zmq.DEALER)
dealer.connect(f'tcp://{xray_config.host}:{xray_config.port}')

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

def remote_start(belt_id):
    from ..instance.config import XrayConfig  # 이동
    xray_config = XrayConfig()  # 이동
    # 로그인 되어 있는지 확인
    if "user_id" not in session:
        return redirect(url_for('login.login_user'))  
    
    # Start 메시지 전송
    dealer.send_string(xray_config.start_message)
    
    # 응답 받기
    response = dealer.recv_string()
    
    if response == "Start Success":
        flash("Start Success!")
    else:
        flash("Start Fail!")
    
    return redirect(url_for('remote.belt_detail', belt_id= belt_id))

def remote_stop(belt_id):
    # 로그인 되어 있는지 확인
    if "user_id" not in session:
        return redirect(url_for('login.login_user'))  
    
    # Stop 메시지 전송
    dealer.send_string(xray_config.stop_message)
    
    # 응답 받기
    response = dealer.recv_string()
    
    if response == "Stop Success":
        flash("Stop Success!")
    else:
        flash("Stop Fail!")
    
    return redirect(url_for('remote.belt_detail', belt_id= belt_id))  

def request_xray_data(belt_id):
    # Edge Server에 요청을 보냅니다.
    dealer.send_string("Request X-ray Data")

    # 받은 응답을 파싱하여 이미지 데이터를 획득합니다.
    response = dealer.recv_string()
    
    status, image_data_base64 = response.split(":")

    if status == "Success":
        # Base64로 인코딩된 이미지 데이터를 디코딩합니다.
        image_data = base64.b64decode(image_data_base64)

        # 이미지 데이터를 PIL Image 객체로 변환합니다.
        image = Image.open(io.BytesIO(image_data))
        
        # 여기서 원하는 포맷(tiff, JPEG 등)으로 저장하거나 처리할 수 있습니다.
        numpy_data = np.array(image)
        
        # 처리된 데이터를 메인 서버로 전송
        send_numpy_data_to_main_server(numpy_data)
        
        return "Data processing successful!", 200
    else:
        return "Failed to request data from Edge Server!", 400
