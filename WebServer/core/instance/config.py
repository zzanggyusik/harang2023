class Network():
    def __init__(self, host, port):
        self.__host: str = host
        self.__port: int = port 
    
    @property
    def host(self):
        return self.__host
    
    @host.setter
    def host(self, value):
        self.__host = value
    
    @property    
    def port(self):
        return self.__port
    
    @port.setter
    def port(self, value):
        self.__port = value
    

# Flask Config    
class FlaskConfig(Network):
    def __init__(self, _host = "0.0.0.0", _port = 5050):
        super().__init__(_host, _port)
        self.__secret_key: str = "harang123!!"  
        self.__session_type: str  = "filesystem"
        
    @property
    def secret_key(self):
        return self.__secret_key
    
    @secret_key.setter
    def secret_key(self, value):
        self.__secret_key = value
        
    @property
    def session_type(self):
        return self.__session_type
    
    @session_type.setter
    def session_type(self, value):
        self.__session_type = value


# MongoDB Config
class MongoDBConfig(Network):    
    def __init__(self, _host = "172.17.14.167", _port = 27017):
        super().__init__(_host, _port)
        
class XrayConfig(Network):
    def __init__(self, host= "172.17.154.192", port= 9297):
        super().__init__(host, port)
        
        self.message = "shot"