import zmq
from .instance.server_config import ServerConfig

class XrayController:
    def __init__(self) -> None:
        self.server_config = ServerConfig()
        
        self.context = zmq.Context()
        
    def server_open(self):
        ROUTER_IP = self.server_config.img_router_ip
        ROUTER_PORT = self.server_config.img_router_port
        self.router = self.context.socket(zmq.ROUTER)
        self.router.bind(f'tcp://{ROUTER_IP}:{ROUTER_PORT}')
        
    def shot(self, ip):
        SHOT_IP = ip
        SHOT_PORT = self.server_config.shot_port
        gun_time = self.server_config.gun_time
        
        self.paster = self.context.socket(zmq.DEALER)
        self.paster.connect(f'tcp://{SHOT_IP}:{SHOT_PORT}')
        
        data = {
            "gun_time" : gun_time,
            "shot_message" : self.server_config.shot_message
        } # TODO Message 보내고 반영
        
        self.paster.send_string(self.server_config.shot_message)
        