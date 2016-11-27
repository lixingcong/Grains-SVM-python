#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月27日
@author: li
'''

from class_features import my_Features


features=my_Features(None,'../data/grain_features.csv')

features.load_features()

y,x=features.get_features_y_x()

with open('../data/sample_libsvm.txt','w') as f:
	for i in range(len(y)):
		feature=x[i]
		this_y=int(y[i])
		f.write(str(this_y)+" ")
		
		for j in range(len(feature)):
			f.write(str(j+1)+":")
			f.write(str(feature[j])+" ")
			
		f.write('\n')
			
		