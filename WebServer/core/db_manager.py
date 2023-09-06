from pymongo import MongoClient, DESCENDING
from flask import session
from .instance.config import MongoDBConfig
from .instance.db_config import *
from dateutil.parser import parse
from bson import ObjectId


class DBManager:
    def __init__(self):
        self.mongoDB = MongoDBConfig()
        self.mongo_client = MongoClient(self.mongoDB.host, self.mongoDB.port)

    def create(self, db, collection, value, key = None, mode = Mode.ONE):
        try:
            if mode == Mode.ONE:
                return self.mongo_client[db][collection].insert_one(value)
            elif mode == Mode.MANY:
                return self.mongo_client[db][collection].insert_many(value)
            
        except:
            return "DB Create: Error Occurred"
    
    def read(self, db= None, collection= None, key= None, value= None, mode = Mode.ONE):
        try:
            if mode == Mode.ONE:
                if key:
                    return self.mongo_client[db][collection].find_one({key: value})
                else:
                    return self.mongo_client[db][collection].find_one()
                
            elif mode == Mode.MANY:
                if key:
                    return self.mongo_client[db][collection].find({key: value})
                else:
                    return self.mongo_client[db][collection].find()
                
            elif mode == Mode.ALL_DATABASES:
                return self.mongo_client.list_database_names()
            
        except:
            return "DB Read: Error Occuarred"
    
    def update(self, db, collection, key_where, value_where, \
                key_set, value_set):
        try:
            return self.mongo_client[db][collection].update_one({key_where: value_where}, {'$set': {key_set: value_set}})
        except:
            return "DB Update: Error Occurred"
    
    def delete(self, db, collection, key, value, mode = Mode.ONE):
        try:
            if mode == Mode.ONE:
                return self.mongo_client[db][collection].delete_one({key: value})

            elif mode == Mode.MANY:
                return self.mongo_client[db][collection].delete_many({key: value})
            
        except:
            return "DB Delete: Error Occurred"
    
    def get_user_convayor_belts(self, user_id):
        return [db for db in self.read(mode= Mode.ALL_DATABASES) if user_id in db]        
    
    def get_user_recent_belt_log(self, database):
        return sorted(self.mongo_client[database].list_collection_names(), reverse= True)[0]   
    
    def get_user_recent_belts_image(self, user_id) -> dict:
        recent_belts_info = {}
        
        user_convayor_belts = self.get_user_convayor_belts(user_id)
        
        for index, database in enumerate(user_convayor_belts):
            recent_belt_log = self.get_user_recent_belt_log(database)    
            
            if recent_belt_log == "Config":
                data= None
            else:
                data= self.mongo_client[database][recent_belt_log].find_one(sort= [("time_uploaded", DESCENDING)])
            
            recent_belts_info[database] = data
            
        return recent_belts_info
            
    def get_user_running_belts(self, user_id) -> dict:
        current_running_belts_number = 0
        user_convayor_belts = [db for db in self.read(mode= Mode.ALL_DATABASES) if user_id in db]   
         
        for database in user_convayor_belts:
            config = self.read(db= database, collection=Collection.Config)
            if config["running_state"]:
                current_running_belts_number += 1
                
        return current_running_belts_number, len(user_convayor_belts)
        
    
    # 사용자 추가
    # def create_user(self, user_data):
    #     return self.user_db.insert_one(user_data)

    # # 사용자 고유 ID로 사용자 조회
    # def find_user_by_id(self, user_id):
    #     return self.user_db.find_one({'_id': user_id})

    # # 사용자 이름(ID)으로 사용자 조회
    # def find_user_by_username(self, username):
    #     return self.user_db.find_one({'username': username})
    
    # # 사용자 로그인 상태 및 로그인 시간 업데이트
    # def update_user_login(self, user_id, login_time):
    #     self.user_db.update_one({'_id': user_id}, {'$set': {'login_time': login_time}})
    #     session['user_id'] = user_id
    #     session['login_time'] = login_time

    # # 벨트 추가
    # def create_belt(self, belt_data):
    #     return self.belt_db.insert_one(belt_data)

    # # 벨트 고유 ID로 벨트 조회
    # def find_belt_by_id(self, belt_id):
    #     return self.belt_db.find_one({'_id': belt_id})

    # def find_belts_by_user_id(self, user_id):
    #     return self.belt_db.find({'user_id': ObjectId(user_id)})

    # # 벨트 삭제
    # def delete_belt(self, belt_id):
    #     return self.belt_db.delete_one({'_id': belt_id})

    # # 사용자 고유 ID로 소유한 벨트 데이터 및 최신 이미지 경로 조회
    # def get_belts_image_data(self, user_id):
    #     belts_data = []
    #     belt_coll = self.belt_db
    #     belt_docs = belt_coll.find({'user_id': user_id})
    #     for belt_doc in belt_docs:
    #         if 'images' in belt_doc and belt_doc['images']:
    #             belt_doc['images'].sort(key=lambda x: parse(x['time_uploaded']), reverse=True)
    #             belts_data.append({
    #                 'belt_id': belt_doc['_id'],
    #                 'image_path': belt_doc['images'][0]['url']  # 'url' 필드로 접근
    #             })
    #     return belts_data
    
    # def create_belt(self, belt_data):
    #     # 동일한 사용자의 동일한 벨트 이름 확인
    #     existing_belt = self.belt_db.find_one({'user_id': belt_data['user_id'], 'belt_name': belt_data['belt_name']})
    #     if existing_belt:
    #         # 이미 존재하는 벨트 이름이라면 에러 반환
    #         return {"error": "Belt name already exists for this user."}

    #     # 벨트 추가
    #     self.belt_db.insert_one(belt_data)
    #     return {"success": True}
    
    # # 사용자 및 해당 사용자의 모든 벨트 데이터 삭제
    # def delete_user_and_belts(self, user_id):
    #     # 회원 정보 삭제
    #     self.user_db.delete_one({'_id': user_id})

    #     # 해당 회원의 모든 벨트 데이터 삭제
    #     self.belt_db.delete_many({'user_id': user_id})


    # # 사용자 아이디를 통한 사용자 벨트조회
    # def find_belt_by_name_and_user_id(self, belt_name, user_id):
    #     return self.belt_db.find_one({'belt_name': belt_name, 'user_id': ObjectId(user_id)})