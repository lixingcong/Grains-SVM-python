#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月23日
@author: li
'''

import cv2
import numpy as np
from class_csv import my_CSV 

class StatModel(object):
	'''parent class - starting point to add abstraction'''    
	def load(self, filename):
		self.model.load(filename)
	def save(self, filename):
		self.model.save(filename)

class my_SVM(StatModel):
	'''wrapper for OpenCV SimpleVectorMachine algorithm'''
	def __init__(self):
		self.model = cv2.SVM()
	
	def train(self, train_x, train_y, C=None, gamma=None):
		param_C = 1 if C is None else C
		param_gamma = (1.0 / len(train_x[0])) if gamma is None else gamma 
		
		print "C, gamma=", param_C, ",", param_gamma
		
		# setting algorithm parameters
		params = dict(kernel_type=cv2.SVM_RBF,
		               svm_type=cv2.SVM_C_SVC,
		               C=param_C,
		               gamma=param_gamma
		               )
		self.model.train(train_x, train_y, params=params)
	
	def predict(self, test_x):
		return np.float32([self.model.predict(s) for s in test_x])
	
if __name__ == '__main__':
	trained_model_filename="cv2_svm_model.xml"
	is_need_to_save=False
	
	train_y, train_x = [], []
	train_number = 0
	test_y, test_x = [], []
	test_number = 0
	
	my_svm=my_SVM()
	
	choose=raw_input("1 for load data from csv, 2 for load model from xml")
	if choose == "1":
		csv_train=my_CSV('../data/my_cut_off/train_1000.csv')
		for line in csv_train.read(1, csv_train.get_total_rows()):
			# pre-process: scale img's grayscale to [0,1]
			img = [x / 255.0 for x in map(float, line[1:])]
			train_y.append(int(line[0]))
			train_x.append(img)
			train_number += 1
		
		# opencv only support np.array array
		train_x = np.asarray(train_x, np.float32)
		train_y = np.asarray(train_y, np.float32)
		
		# train all data
		my_svm.train(train_x, train_y,C=1,gamma=0.026)
		is_need_to_save=True
	else:
		my_svm.load(trained_model_filename)
		
	# load test data
	csv_test=my_CSV('../data/my_cut_off/test_100.csv')
	for line in csv_test.read(1, csv_test.get_total_rows()):
		# pre-process: scale img's grayscale to [0,1]
		img = [x / 255.0 for x in map(float, line[1:])]
		test_y.append(int(line[0]))
		test_x.append(img)
		test_number += 1
	test_x = np.asarray(test_x, np.float32)
		
	# predict
	predict_values_nparray = my_svm.predict(test_x)
	predict_values = predict_values_nparray.tolist()
	
	predict_error_counter = 0
	for index in range(test_number):
		predict_val, test_y_ = predict_values[index], test_y[index]
		if abs(predict_val - test_y_) > 0.001:
			print "[WRONG] predict=%f, test_y=%f" % (predict_val, test_y_)
			predict_error_counter += 1
			
	print "train_num=%d, test_num=%d, predict_correct_num=%d" % (train_number, test_number, test_number - predict_error_counter)
	print "predict accuracy=%.1f%%" % (100 * float(test_number - predict_error_counter) / test_number)
	
	# save trained model
	if is_need_to_save:
		my_svm.save("cv2_svm_model.xml")	
