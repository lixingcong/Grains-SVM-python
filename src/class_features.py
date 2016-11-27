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
from class_crop import my_Crop
from color_prop import get_rgb_normolized
import cv2

# CSV: splited by common
#
# saved csv file columns
# ------------------------------------------------
# | category | color:R | color:G | Hu(1) | riLBP |
# ------------------------------------------------
# 
# itemlist csv file columns, when category is 0, it means unknown
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
		
		self.lbp_calculator=my_RILBP()
		self.mycrop=my_Crop(blocks_split=[3,3])
		
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
			this_feature=[]
			img=my_Preprocess(filename)
			# RGB fetures
			R,G,B=get_rgb_normolized(img.get_img(), img.get_img_binary())
			this_feature.append(R)
			this_feature.append(G)
			# Hu(1)
			myshape=my_SHAPE(img.get_img_gray(), img.get_img_binary())
			Hu_1=myshape.get_humoments()
			this_feature.append(Hu_1)
			# LBP			
			img_splited=self.mycrop.get_cropped_images(img.get_img_gray())
			for img_ in img_splited:
				lbp_histogram=self.lbp_calculator.get_lbp_histogram(img_)
				for histogram_y in lbp_histogram:
					this_feature.append(histogram_y)
			
			print this_feature
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
	
