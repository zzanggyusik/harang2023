import zmq
from config import *

class XrayController:
    def __init__(self):
        self.context = zmq.Context()
        self.dealer = self.context.socket(zmq.DEALER)
        self.dealer.connect(f'tcp://{HOST_IP}:{PORT}')
        
    def shot(self):
        message = MESSAGE
        self.dealer.send_string(message)
        print(f'Message : {message} is sent to {HOST_IP}:{PORT}')