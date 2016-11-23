#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月23日
@author: li
'''

import cv2
import csv
from svm_class import mySVM
import numpy as np

'''
train_y, train_x = [], []
test_y, test_x = [], []

# raw data: train
with open('../data/my_cut_off/train_1000.csv', 'rb')as f_csv:
	train_csv = csv.reader(f_csv, delimiter=',')
	for line in train_csv:
		# scale img to [0,1]
		img = [x / 255.0 for x in map(float,line[1:])]
		train_y.append(int(line[0]))
		train_x.append(img)

# raw data: test
with open('../data/my_cut_off/test_100.csv', 'rb')as f_csv:
	test_csv = csv.reader(f_csv, delimiter=',')
	for line in test_csv:
		# scale img to [0,1]
		img = [x / 255.0 for x in map(float,line[1:])]
		test_y.append(int(line[0]))
		test_x.append(img)
'''
train_y = np.array([1,1,-1],dtype=np.float32)
train_x = np.array(
				[[4,3],
				 [3,3],
				 [1,1]],
				dtype=np.float32)
test_x = np.array([[0,0],],dtype=np.float32)

clf = mySVM()
clf.train(train_x, train_y)
y_val = clf.predict(test_x)

for i in y_val:print i

# svm train

