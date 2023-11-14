import tensorflow as tf
import os, sys
from config import *
import cv2
import numpy as np
import time

class App():
    def __init__(self):
        self.get_model()
        self.cam_open()

    def cam_open(self):
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            
            h, w, _ = frame.shape
            start_x = max(0, (w - 300) // 2)
            start_y = max(0, (h - 300) // 2)
            
            cropped_frame = frame[start_y:start_y+300, start_x:start_x+300]

            img = cv2.resize(cropped_frame, (224, 224))
            img = img / 255.0
            img = np.expand_dims(img, axis=0)
            
            pred = self.prediction(img)
            
            cv2.rectangle(frame, (start_x, start_y), (start_x+224, start_y+224), (0, 255, 0), 2)
            
            print(pred)
            
            if pred[0][0] > 0.5 :
                print(type(pred))
                print(pred[0][0])
                print('banana')
                pass
            
            else :
                print(type(pred))
                print(pred[0][0])
                print('grapefruit')

            cv2.imshow("Apple Detection", frame)

            # 'q' 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            #time.sleep(1)

        # 작업 완료 후 카메라 해제
        cap.release()
        cv2.destroyAllWindows()
            
    def get_model(self):
        self.model = tf.keras.models.load_model(AppConfig.model)
        
    def prediction(self, img):
        result = self.model.predict(img)
        
        return result
    
App()