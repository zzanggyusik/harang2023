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