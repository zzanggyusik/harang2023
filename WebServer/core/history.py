from flask import Blueprint, render_template, session, redirect, url_for, request
from .db_manager import DBManager
from .instance.db_config import *
from dateutil.parser import parse

history = Blueprint("history", __name__, url_prefix="/history")

db_manager = DBManager()

@history.route('/', methods=['GET'])
def show_history():
    if "user_id" not in session:
        return redirect(url_for('login.login_user'))    
    
    belts_db = db_manager.get_user_convayor_belts(session["user_id"])
    belts_thumbnail = {}
    for db in belts_db:
        collection = [col for col in db_manager.mongo_client[db].list_collection_names() if col not in "Config"]
        
        history_data = {}
        # thumbnail_dict = {}
        for col in collection:
            # 콜렉션에 있는 도큐먼트 수 
            document_count = db_manager.mongo_client[db][col].estimated_document_count()
            
            if document_count <= 1:
                # thumbnail_dict[col]= db_manager.read(db= db, collection= col)
                history_data[col] = db_manager.read(db= db, collection= col)
            
            # elif document_count < 6:
            #     thumbnail_dict[col]= list(db_manager.read(db= db, collection= col, mode= Mode.MANY))
                
            else:
                history_data[col] = list(db_manager.read(db= db, collection= col, mode= Mode.MANY))
                # thumbnail_dict[col]= list(db_manager.read(db= db, collection= col, mode= Mode.MANY)[:6])
            
            # belts_thumbnail[db] = thumbnail_dict 
            belts_thumbnail[db] = history_data 
            
                    
    print(f"belts thumbnail = {belts_thumbnail}")
    
    return render_template('history.html', belts_thumbnail= belts_thumbnail)

@history.route('/detail', methods=['GET'])
def history_detail():
    db= request.args.get("db")
    col= request.args.get("col")
    
    document_data = list(db_manager.read(db= db, collection= col, mode= Mode.MANY)) 
    
    print("document data", document_data)
    
    return render_template('history_detail.html', document_data= document_data)

@history.route('/detail/image', methods=['GET'])
def show_history_detail_image():
    return render_template('history_detail_image.html')

def get_history_blueprint():
    return history