#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月27日
@author: li
特征基类
'''

from class_csv import my_CSV
from class_preprocess import my_Preprocess
from class_rilbp import my_RILBP
from class_shape import my_SHAPE
from class_svm import my_SVM
from class_crop import my_Crop
import cv2

# CSV: splited by common
#
# saved csv file columns
# ------------------------------------------------
# | category | color:R | color:G | Hu(1) | riLBP |
# ------------------------------------------------
# 
# itemlist csv file colums
# -------------------------------------------
# | Chinese | category | filename | is_good |
# -------------------------------------------

class my_Features(object):
	def __init__(self,csv_itemlist,csv_features_save):
		self.csv_itemlist=csv_itemlist
		self.csv_features_save=csv_features_save
		self.itemlist=[]
		self.dict_category_to_chinese={}
		self.features=[]
		self.x=[]
		self.y=[]
		
	def get_chinese_from_category(self,c):
		return self.dict_category_to_chinese[c]
		
	def load_itemlist(self):
		my_csv=my_CSV(self.csv_itemlist)
		for line in my_csv.read(1,my_csv.get_total_rows()):
			self.itemlist.append(line)
			self.dict_category_to_chinese[line[1]]=line[0]
	
	def save_features(self):
		pass
	
	def calc_features(self):
		for item in self.itemlist:
			filename=item[2]
			img=my_Preprocess(filename)
			self._show_img(img.get_img())
			break
			
	def _show_img(self,img):
		cv2.namedWindow('img', cv2.WINDOW_NORMAL)
		cv2.resizeWindow('img', 300, 300)
		cv2.imshow('img',img)
		if cv2.waitKey(0) == 27:
			cv2.destroyAllWindows()
		
if __name__ == '__main__':
	my_features=my_Features('../data/grain_list.csv', '../data/grain_features.csv')
	my_features.load_itemlist()
	my_features.calc_features()
	
