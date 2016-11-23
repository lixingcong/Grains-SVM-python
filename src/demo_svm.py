#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月23日
@author: li
'''

import csv
from svm_class import mySVM
import numpy as np

train_y, train_x = [], []
train_number = 0
test_y, test_x = [], []
test_number = 0

# raw data: train
with open('../data/my_cut_off/train_1000.csv', 'rb')as f_csv:
	train_csv = csv.reader(f_csv, delimiter=',')
	for line in train_csv:
		# scale img to [0,1]
		img = [x / 255.0 for x in map(float, line[1:])]
		train_y.append(int(line[0]))
		train_x.append(img)
		train_number += 1

# raw data: test
with open('../data/my_cut_off/test_100.csv', 'rb')as f_csv:
	test_csv = csv.reader(f_csv, delimiter=',')
	for line in test_csv:
		# scale img to [0,1]
		img = [x / 255.0 for x in map(float, line[1:])]
		test_y.append(int(line[0]))
		test_x.append(img)
		test_number += 1

train_x = np.asarray(train_x, np.float32)
train_y = np.asarray(train_y, np.float32)
test_x = np.asarray(test_x, np.float32)

clf = mySVM()
clf.train(train_x, train_y)
predict_values_nparray = clf.predict(test_x)

predict_values = predict_values_nparray.tolist()

predict_error_counter = 0
for index in range(test_number):
	predict_val, test_y_ = predict_values[index], test_y[index]
	if abs(predict_val - test_y_) > 0.001:
		print "[WRONG] predict=%f, test_y=%f" % (predict_val, test_y_)
		predict_error_counter += 1
		
print "train_num=%d, test_num=%d, predict_correct_num=%d" % (train_number, test_number, test_number - predict_error_counter)
print "predict accuracy=%.1f%%" % (100 * float(test_number - predict_error_counter) / test_number)

# svm train

