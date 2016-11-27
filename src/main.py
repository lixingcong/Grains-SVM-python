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

if __name__ == '__main__':
	svm=my_SVM()
	trained_model_filename="cv2_svm_model.xml"
	
	features_train=my_Features('../data/grain_list.csv', '../data/grain_features.csv')
	features_train.load_features()
	
	train_y,train_x=features_train.get_features_y_x()
	
	# opencv only support np.array array
	train_x = np.asarray(train_x, np.float32)
	train_y = np.asarray(train_y, np.float32)
	
	# train all data
	svm.train(train_x, train_y)
	
	choose=raw_input("Would you like to save model? (y/n)")
	if choose == 'y':
		svm.save(trained_model_filename)
		print "saved"
