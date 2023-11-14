import tensorflow as tf
import os
from config import *
import cv2
import numpy as np
from sklearn.metrics import accuracy_score
import seaborn as sns
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

class AITest():
    def __init__(self):
        mode = input(f'G : Grapefrit  B : Banana\n').lower()
        if mode == 'g':        
            self.get_dataset('Grapefruit White')
        elif mode == 'b':
            self.get_dataset('Banana')
        self.get_best_model()
        self.test()
    
    def get_dataset(self, category):
        self.image_w = 224
        self.image_h = 224
        
        self.category = category
        
        self.file_list = os.listdir(f'{TestConfig.root_dir}/{category}')     
        
    def get_best_model(self):
        self.best_model = tf.keras.models.load_model(TestConfig.model)
        
    def create_confusion_matrix(self, true_labels):
        predicted_labels = []  # 예측된 레이블을 저장할 리스트
        for file_name in self.file_list:
            input_img = cv2.imread(f'{TestConfig.root_dir}/{self.category}/{file_name}')
            input_img = cv2.imread(f'{TestConfig.root_dir}/{self.category}/{file_name}')
            input_img = cv2.resize(input_img, None, fx=self.image_w/input_img.shape[1], fy=self.image_h/input_img.shape[0])
            input_img = np.array(input_img)
            input_img = input_img.reshape(-1, TestConfig.reshape('x'), TestConfig.reshape('y'), TestConfig.reshape('channel'))
            input_img = input_img.astype(TestConfig.reshape('astype'))
            input_img /= 255
            
            predict_result = self.best_model.predict(input_img)
            predicted_labels.append(np.argmax(predict_result, axis=1))  # 가장 높은 확률의 클래스 인덱스 추가
            
        predicted_labels = np.concatenate(predicted_labels)  # 리스트를 넘파이 배열로 변환
        cm = confusion_matrix(true_labels, predicted_labels)
        
        # Confusion matrix 출력
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=range(len(TestConfig.classes)), yticklabels=range(len(TestConfig.classes)))
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix')
        plt.show()    
        
    def test(self):
        result = []
        true_labels = []
        
        for file_name in self.file_list:
            input_img = cv2.imread(f'{TestConfig.root_dir}/{self.category}/{file_name}')
            input_img = cv2.resize(input_img, None, fx=self.image_w/input_img.shape[1], fy=self.image_h/input_img.shape[0])
            input_img = np.array(input_img)
            input_img = input_img.reshape(-1, TestConfig.reshape('x'), TestConfig.reshape('y'), TestConfig.reshape('channel'))
            input_img = input_img.astype(TestConfig.reshape('astype'))
            input_img /= 255
            
            predict_result = self.best_model.predict(input_img)
            result.append(predict_result)
            true_labels.append(TestConfig.classes.index(self.category))
            
            #print(predict_result)
            
        #print(result)
        self.create_confusion_matrix(true_labels)
        
    
AITest()