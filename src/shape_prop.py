#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月26日
@author: li
描述形状：
Hu不变矩：
  - 具有平移、旋转、尺度不变性
  - 得出7个分量，但是实际应用中只用前2个分量
'''

import cv2
from class_preprocess import my_Preprocess
import numpy as np

class my_SHAPE(object):
	def __init__(self,img_gray,img_bin,canny_thresh=127):
		self.img=img_gray
		self.img_bin=img_bin
		self.contours=None
		self.hierarchy=None
		self.canny_thresh=canny_thresh
		self.thresh_max=255
		
		self._morphology(radius=5)
		
	# 找出轮廓
	def _find_contours(self,thresh):
		edges = cv2.Canny(self.img_bin,thresh,thresh*2)
		self.contours,self.hierarchy=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		
	def _morphology(self, radius):
		# kernel = np.ones((radius, radius), np.uint8)
		kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(radius,radius))
		self.img_bin = cv2.morphologyEx(self.img_bin, cv2.MORPH_OPEN, kernel)
	
	# 创建input output窗体
	def _create_2_windows(self,width):
		cv2.namedWindow('input',cv2.WINDOW_NORMAL)
		cv2.resizeWindow('input', width,width)
		cv2.namedWindow('output',cv2.WINDOW_NORMAL)
		cv2.resizeWindow('output', width,width)
		
	def _show_all_windows(self):
		if cv2.waitKey(0) == 27:
			cv2.destroyAllWindows()

	# 滑动Trackbar的回调函数，动态绘制不同canny阈值的边缘图像
	def _callback_draw_contours(self,thresh):
		# https://github.com/abidrahmank/OpenCV2-Python/blob/master/Official_Tutorial_Python_Codes/3_imgproc/moments.py
		self._find_contours(thresh)
		
		drawing = np.zeros(self.img.shape,np.uint8)                  # Image to draw the contours
		for cnt in self.contours:
			moments = cv2.moments(cnt)                          # Calculate moments
			if moments['m00']!=0:
				cx = int(moments['m10']/moments['m00'])         # cx = M10/M00
				cy = int(moments['m01']/moments['m00'])         # cy = M01/M00
				moment_area = moments['m00']                    # Contour area from moment
				print moment_area
				# contour_area = cv2.contourArea(cnt)             # Contour area using in_built function
				cv2.drawContours(drawing,[cnt],0,255,1)   # draw contours 
				cv2.circle(drawing,(cx,cy),3,50,-1)      # draw centroids
		
		cv2.imshow('output',drawing)
		cv2.imshow('input',self.img)
		print '-'*20
		
	# 带有滑动Trackbar的绘制边缘
	def draw_contours(self,thresh_max=None):
		if thresh_max is None:
			thresh_max=self.thresh_max
			
		# 添加一个属性可以调节窗口大小
		windows_width=300
		self._create_2_windows(windows_width)
		
		cv2.namedWindow('bar',cv2.WINDOW_NORMAL)
		cv2.resizeWindow('bar', 400,10)
		cv2.createTrackbar('canny_thresh:','bar',self.canny_thresh,thresh_max,self._callback_draw_contours)
		
		self._callback_draw_contours(self.canny_thresh)
		
		self._show_all_windows()

	# 绘制面积最大的边缘
	def draw_contours_largest(self):	
		self._find_contours(self.canny_thresh)
		area_largest=0
		area_largest_cnt=[]
		drawing = np.zeros(self.img.shape,np.uint8)                  # Image to draw the contours
		
		for cnt in self.contours:
			moments = cv2.moments(cnt)                          # Calculate moments
			if moments['m00']!=0:
				moment_area = moments['m00']                    # Contour area from moment
				if area_largest<moment_area:
					area_largest=moment_area
					area_largest_cnt=cnt
				
		cv2.drawContours(drawing,[area_largest_cnt,],0,255,1)   # draw contours 
			
		# 添加一个属性可以调节窗口大小
		windows_width=300
		self._create_2_windows(windows_width)
		cv2.imshow('output',drawing)
		cv2.imshow('input',self.img)
		self._show_all_windows()

if __name__ == '__main__':
	mypreprocess=my_Preprocess("../data/s.png",[48,48])
	cv2.imshow("bin",mypreprocess.get_img_binary())
	myshape=my_SHAPE(mypreprocess.get_img_gray(),mypreprocess.get_img_binary())	
# 	myshape.draw_contours()
	myshape.draw_contours_largest()
