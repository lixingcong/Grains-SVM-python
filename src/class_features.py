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
from utils import get_rgb_normolized, normalize_from_list
import cv2

# CSV: splited by common
#
# saved features csv file columns
# ----------------------------------------------------------
# | Chinese | category | color:R | color:G | Hu(1) | riLBP |
# ----------------------------------------------------------
# 
# itemlist csv file columns, when category or Chinese are both 0, it means unknown item
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
		c=str(int(c))
		return self.dict_category_to_chinese[c]
	
	def get_features_y_x(self):
		if self.y == []:
			print "features is Empty, Now loading from itemlist..."
			self.calc_features_for_itemlist()
		
		return (self.y, self.x)
		
	def load_itemlist(self):
		my_csv=my_CSV(self.csv_itemlist)
		for line in my_csv.read(1,my_csv.get_total_rows()):
			self.itemlist.append(line)
			# grain category is known
			if line[1] != '0':
				self.dict_category_to_chinese[line[1]]=line[0]
	
	def save_features(self):
		if self.features == []:
			print "features is Empty, Now loading from itemlist..."
			self.calc_features_for_itemlist()
			
		my_csv=my_CSV(self.csv_features_save)
		
		data=[]
		for i in range(len(self.y)):
			this_line=[]
			this_line.append(self.get_chinese_from_category(self.y[i]))
			this_line.append(self.y[i])
			for j in self.x[i]:
				this_line.append(j)
			data.append(this_line)
		
		my_csv.write(data)
		
	def load_saved_features(self):
		my_csv=my_CSV(self.csv_features_save)
		for line in my_csv.read(1,my_csv.get_total_rows()):
			self.features.append(line)
			self.dict_category_to_chinese[line[1]]=line[0]
		
		self._load_y_x_from_features()
			
	def _load_y_x_from_features(self):
		for line in self.features:
			self.x.append(line[2:])
			self.y.append(int(line[1]))	
	
	def calc_features_for_itemlist(self):
		index=1
		index_max=len(self.itemlist)
		for item in self.itemlist:
			if item[3]=='0':
				continue
			
			filename=item[2]
			this_feature=[]
			
			# mark this category
			this_feature.append(item[0])
			this_feature.append(item[1])
			
			# open a img and pre-process
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
			img_foreground=myshape.get_foreground()
			img_resized=cv2.resize(img_foreground, (48, 48), interpolation=cv2.INTER_CUBIC)
			img_splited=self.mycrop.get_cropped_images(img_resized)			
			for img_ in img_splited:
				lbp_histogram=self.lbp_calculator.get_lbp_histogram(img_)
				for histogram_y in lbp_histogram:
					this_feature.append(histogram_y)
						
			self.features.append(this_feature)
			
			# counter
			print "%d/%d"%(index,index_max)
			index+=1
		
		self._load_y_x_from_features()
		self._normalize_x()

	def _normalize_x(self):
		self.x = normalize_from_list(self.x)
		
if __name__ == '__main__':
	my_features=my_Features('../data/grain_list.csv', '../data/grain_features.csv')
	#my_features.load_itemlist()
	my_features.load_saved_features()
	#my_features.calc_features_for_itemlist()
	#my_features.save_features()
	print my_features.get_features_y_x()[0]
	print my_features.get_chinese_from_category(1)
	
