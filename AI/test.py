import tensorflow as tf
import os, sys
from config import *
import cv2
import numpy as np
from sklearn.metrics import accuracy_score
import seaborn as sns
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

class AITest():
    def __init__(self):
        self.get_dataset('apple')
        self.get_best_model()
        self.test()
    
    def get_dataset(self, category):
        self.image_w = 224
        self.image_h = 224
        
        self.category = category
        
        self.org_file_list = os.listdir(f'{TestConfig.test_dir}')
        self.file_list = [file for file in self.org_file_list if file.endswith(TestConfig.ex)]
                
        print(self.file_list)
        
    def get_best_model(self):
        self.best_model = tf.keras.models.load_model(TestConfig.model)
        
    def test(self):
        file_name = self.file_list[0]
        
        input_img = cv2.imread(f'{TestConfig.test_dir}/{file_name}')
        input_img = cv2.resize(input_img, None, fx=self.image_w/input_img.shape[1], fy=self.image_h/input_img.shape[0])
        input_img = np.array(input_img)
        input_img = input_img.reshape(-1, TestConfig.reshape('x'), TestConfig.reshape('y'), TestConfig.reshape('channel'))
        input_img = input_img.astype(TestConfig.reshape('astype'))
        input_img /= 255
        
        predict_result = self.best_model.predict(input_img)
        for i in range(len(predict_result)):
            predict_result[i] = np.round(predict_result[i])
        print(predict_result)
        
    
AITest()