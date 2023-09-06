from XrayController import XrayController
import time

while True:
    xray = XrayController()
    xray.shot()
    time.sleep(2)