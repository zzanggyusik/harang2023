from pyrtsp import RtspServer
from config import *

class CustomRtspServer(RtspServer):
    def __init__(self, ip, port):
        super().__init__(ip, port)

if __name__ == "__main__":
    ip = HOST_IP
    port = PORT
    server = CustomRtspServer(ip, port)
    server.run()