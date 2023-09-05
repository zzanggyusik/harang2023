import zmq
from .instance.server_config import ServerConfig

class XrayController:
    def __init__(self) -> None:
        self.server_config = ServerConfig()
        ROUTER_IP = self.server_config.img_router_ip
        ROUTER_PORT = self.server_config.img_router_port
        self.context = zmq.Context()
        
    def server_open(self):
        
    def shot(self):