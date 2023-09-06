import zmq
from .instance.config import *

class XrayController:
    def __init__(self):
        self.xray_config = XrayConfig()
        
        self.context = zmq.Context()
        self.dealer = self.context.socket(zmq.DEALER)
        self.dealer.connect(f'tcp://{self.xray_config.host}:{self.xray_config.port}')
        
    def shot(self):
        print("Shot Activated")
        message = self.xray_config.message
        self.dealer.send_string(message)
