#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月27日
@author: li
将csv文件转成libsvm专用的训练样本文件
用于调用libsvm的grid.py进行交叉验证获得最佳C和gamma
'''

from class_features import my_Features

csv_filename='../data/grain_features.csv'
print "Converting "+csv_filename+" to libsvm format..."

features=my_Features(None,csv_filename)

features.load_saved_features()

y,x=features.get_features_y_x()

with open('../data/sample_libsvm.txt','w') as f:
	for i in range(len(y)):
		feature=x[i]
		this_y=int(y[i])
		f.write(str(this_y)+" ")
		
		for j in range(len(feature)):
			if str(feature[j]) != "":
				f.write(str(j+1)+":")
				f.write(str(feature[j])+" ")
			
		f.write('\n')
			
		