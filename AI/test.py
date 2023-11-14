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
        self.image_w = 224
        self.image_h = 224
        self.categories = ['Grapefruit White', 'Banana']
        self.get_best_model()
        self.test()

    def get_best_model(self):
        self.best_model = tf.keras.models.load_model(TestConfig.model)

    def create_confusion_matrix(self, true_labels, predicted_labels):
        cm = confusion_matrix(true_labels, predicted_labels)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=range(len(TestConfig.classes)), yticklabels=range(len(TestConfig.classes)))
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix')
        plt.show()

    def test(self):
        true_labels = []
        predicted_labels = []

        for category in self.categories:
            file_list = os.listdir(f'{TestConfig.root_dir}/{category}')
            
            for file_name in file_list:
                input_img = cv2.imread(f'{TestConfig.root_dir}/{category}/{file_name}')
                input_img = cv2.resize(input_img, (self.image_w, self.image_h))
                input_img = np.array(input_img)
                input_img = input_img.reshape(1, self.image_w, self.image_h, 3).astype('float32') / 255

                predict_result = self.best_model.predict(input_img)
                predicted_labels.append(np.argmax(predict_result, axis=1))
                true_labels.append(TestConfig.classes.index(category))

        true_labels = np.array(true_labels)
        predicted_labels = np.concatenate(predicted_labels)
        self.create_confusion_matrix(true_labels, predicted_labels)

AITest()