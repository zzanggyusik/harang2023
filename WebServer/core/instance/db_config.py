from enum import Enum

class Database():    
    Users = "Users"
    
    def user_conveyorbelt(user, conveyorbelt) -> str:
        return f"{user}_{conveyorbelt}"
        

    

class Collection():
    User = "User"
    Create_info = "Create_info"
        
class Key():
    user_id = "user_id"
    
        
class Mode(Enum):
    ONE = 0
    MANY = 1
    

    

    