#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月23日
@author: li
'''

import cv2
import numpy as np

class StatModel(object):
	'''parent class - starting point to add abstraction'''    
	def load(self, fn):
		self.model.load(fn)
	def save(self, fn):
		self.model.save(fn)

class mySVM(StatModel):
	'''wrapper for OpenCV SimpleVectorMachine algorithm'''
	def __init__(self):
		self.model = cv2.SVM()
	
	def train(self, samples, responses):
		#setting algorithm parameters
		params = dict( kernel_type = cv2.SVM_LINEAR, 
		               svm_type = cv2.SVM_C_SVC,
		               C = 1 
		               )
		self.model.train(samples, responses, params = params)
	
	def predict(self, samples):
		return np.float32( [self.model.predict(s) for s in samples])
