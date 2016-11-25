#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月25日
@author: li
图片ROI分割（Region of Image），效果即Split the image into blocks
'''

import cv2
import sys

class CROP_IMG(object):
	def __init__(self,blks_split=None,pixels_split=None):
		# params:
		# input_img    is an cv2 image object
		# blks_split   is a list [blks_horizontal,   blks_vertical  ]
		# pixels_split is a list [pixels_horizontal, pixels_vertical]
		if blks_split is None:
			assert pixels_split is not None
			self.is_pixel_mode=True
			self.pixels_spilt_horizontal, self.pixels_spilt_vertical=pixels_split
			self.blocks_spilt_horizontal, self.blocks_spilt_vertical=0,0
		else:
			self.is_pixel_mode=False
			self.pixels_spilt_horizontal, self.pixels_spilt_vertical=0,0
			self.blocks_spilt_horizontal, self.blocks_spilt_vertical=blks_split
		
		self.img=None
	
	def _assert_shape(self):
		self.img_height=self.img.shape[0]
		self.img_width=self.img.shape[1]
		
		# shape should be divided correctly
		if self.is_pixel_mode:
			assert (self.img_height % self.pixels_spilt_vertical == 0) 
			assert (self.img_width % self.pixels_spilt_horizontal == 0)
		else:
			assert (self.img_height % self.blocks_spilt_vertical == 0) 
			assert (self.img_width % self.blocks_spilt_horizontal == 0)
		
	def get_cropped_images(self,input_img):
		self.img=input_img
		self._assert_shape()
		splited_blocks=[]
		if self.is_pixel_mode:
			self.blocks_spilt_horizontal = self.img_width / self.pixels_spilt_horizontal
			self.blocks_spilt_vertical = self.img_height / self.pixels_spilt_vertical
		else:
			self.pixels_spilt_horizontal=self.img_width/self.blocks_spilt_horizontal
			self.pixels_spilt_vertical=self.img_height/self.blocks_spilt_vertical
		
		for block_num_vertical in range(self.blocks_spilt_vertical):
			y1=self.pixels_spilt_vertical*block_num_vertical
			y2=y1+self.pixels_spilt_vertical
			
			for block_num_horizontal in range(self.blocks_spilt_horizontal):
				x1=self.pixels_spilt_horizontal*block_num_horizontal
				x2=x1+self.pixels_spilt_horizontal
				# split by pixels
				splited_blocks.append(self.img[y1:y2,x1:x2])
		
		return splited_blocks
if __name__ == '__main__':
	img = cv2.imread("../data/sample.png")
	img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

	print '-'*10
	img_resized = cv2.resize(img_gray, (4, 6), interpolation=cv2.INTER_CUBIC)
	print img_resized
	
# 	crop=CROP_IMG(blks_split=[2,3], pixels_split=None)
	crop=CROP_IMG(blks_split=None, pixels_split=[2,3])
	img_got=crop.get_cropped_images(img_resized)
	#sys.exit(0)
	for i in range(len(img_got)):
		print "----\n#%d:"%i
		print img_got[i]
	
