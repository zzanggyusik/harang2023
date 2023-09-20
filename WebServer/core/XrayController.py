import zmq
from .instance.config import *

class XrayController:
    def __init__(self):
        self.xray_config = XrayConfig()
        
        self.context = zmq.Context()
        self.dealer = self.context.socket(zmq.DEALER)
        self.dealer.connect(f'tcp://{self.xray_config.host}:{self.xray_config.port}')
        
    # belt_id를 추가해서 동기화 방법을 고려해야함.
    # 사용하지 않을거면 아래의 주석 양식대로
    
    # def shot(self):
    #     print("Shot Activated")
    #     message = self.xray_config.message
    #     self.dealer.send_string(message)
    
    def shot(self, belt_id):
        print("Shot Activated {belt_id}")
        message = self.xray_config.message.format(belt_id=belt_id)
        self.dealer.send_string(message)

    def start_belt(self, belt_id):
        print(f"Starting Belt {belt_id}")
        start_message = self.xray_config.start_message.format(belt_id=belt_id)
        self.dealer.send_string(start_message)
        
        # 서버로부터 응답을 수신하고 처리
        response = self.dealer.recv_string()
        if response == "Start Success":
            return "Start Success"
        else:
            return "Start Fail"

    def stop_belt(self, belt_id):
        print(f"Stopping Belt {belt_id}")
        stop_message = self.xray_config.stop_message.format(belt_id=belt_id)
        self.dealer.send_string(stop_message)
        
        # 서버로부터 응답을 수신하고 처리
        response = self.dealer.recv_string()
        if response == "Stop Success":
            return "Stop Success"
        else:
            return "Stop Fail"