#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月27日
@author: li
训练样本主函数
'''

from class_features import my_Features
from class_svm import my_SVM
import numpy as np
import sys

if __name__ == '__main__':
	svm = my_SVM()
	svm_param_C, svm_param_gamma = 2.82842712475,0.25
	
	trained_model_filename = "cv2_svm_model.xml"
	
	features_train = my_Features('../data/grain_psd_list.csv', '../data/grain_features.csv')
# 	features_train.load_itemlist()
# 	features_train.save_features()
	features_train.load_saved_features()
	
	train_y, train_x = features_train.get_features_y_x()
	train_number = len(train_x)
	
	# opencv only support np.array array
	train_x = np.asarray(train_x, np.float32)
	train_y = np.asarray(train_y, np.float32)
	
	# train all data
	svm.train(train_x, train_y, C=svm_param_C, gamma=svm_param_gamma)
	
	# load test csv
	features_test = my_Features('../data/test_list.csv', '../data/test_features.csv')
# 	features_test.load_itemlist()
# 	features_test.save_features()
	features_test.load_saved_features()

	test_y, test_x = features_test.get_features_y_x()
	test_number = len(test_x)
	
	# test
	test_x = np.asarray(test_x, np.float32)
	predict_values_nparray = svm.predict(test_x)
	
	predict_values = predict_values_nparray.tolist()
	
	predict_error_counter = 0
	for index in range(test_number):
		predict_val, test_y_ = predict_values[index], test_y[index]
		if abs(predict_val - test_y_) > 0.001:
			print "[WRONG] predict=%f, test_y=%f" % (predict_val, test_y_)
			predict_error_counter += 1
			
	print "train_num=%d, test_num=%d, predict_correct_num=%d" % (train_number, test_number, test_number - predict_error_counter)
	print "predict accuracy=%.1f%%" % (100 * float(test_number - predict_error_counter) / test_number)
	
	sys.exit(0)
	choose = raw_input("Would you like to save model? (y/n)")
	if choose == 'y':
		svm.save(trained_model_filename)
		print "saved"
