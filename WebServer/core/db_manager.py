from pymongo import MongoClient
from flask import session
from .instance.config import MONGODB_IP, MONGODB_PORT
from dateutil.parser import parse

class DBManager:
    def __init__(self):
        self.client = MongoClient(MONGODB_IP, MONGODB_PORT)
        self.user_db = self.client['harang']['User']
        self.belt_db = self.client['harang']['Belt']

    # 사용자 추가
    def create_user(self, user_data):
        result = self.user_db.insert_one(user_data)
        return result.inserted_id

    # 사용자 고유 ID로 사용자 조회
    def find_user_by_id(self, user_id):
        return self.user_db.find_one({'_id': user_id})

    # 사용자 이름(ID)으로 사용자 조회
    def find_user_by_username(self, username):
        return self.user_db.find_one({'username': username})

    # 사용자 로그인 상태 및 로그인 시간 업데이트
    def update_user_login(self, user_id, login_time):
        self.user_db.update_one({'_id': user_id}, {'$set': {'login_time': login_time}})
        session['user_id'] = user_id
        session['login_time'] = login_time

    # 벨트 추가
    def create_belt(self, belt_data):
        print(belt_data)  # 디버깅을 위해 belt_data 내용 확인
        return self.belt_db.insert_one(belt_data)

    # 벨트 고유 ID로 벨트 조회
    def find_belt_by_id(self, belt_id):
        return self.belt_db.find_one({'_id': belt_id})

    # 사용자 고유 ID로 소유한 벨트 목록 조회
    def find_belts_by_user_id(self, user_id):
        return self.belt_db.find({'user_id': user_id})

    # 벨트 삭제
    def delete_belt(self, belt_id):
        return self.belt_db.delete_one({'_id': belt_id})

    # 사용자 고유 ID로 소유한 벨트 데이터 및 최신 이미지 경로 조회
    def get_belts_data(self, user_id):
        belts_data = []
        belt_coll = self.belt_db
        belt_docs = belt_coll.find({'user_id': user_id})
        for belt_doc in belt_docs:
            if belt_doc['images']: # 이미지 리스트가 비어있지 않은지 확인
                belt_doc['images'].sort(key=lambda x: parse(x['time_uploaded']), reverse=True)
                belts_data.append({
                    'belt_id': belt_doc['_id'],
                    'image_path': belt_doc['images'][0]['image_path']
                })
        return belts_data