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
import sys

class my_SHAPE(object):
	def __init__(self, img_gray, canny_thresh=20):
		self.img = img_gray
		self.contours = None
		self.contours_largest = None
		self.hierarchy = None
		self.canny_thresh = canny_thresh
		self.thresh_max = 255
		
		# TODO: 形态学滤波，预处理，将canny边缘缺口补上？

	# 找出轮廓
	def _find_contours(self, thresh):
		edges = cv2.Canny(self.img, thresh, thresh * 2)
		self.contours, self.hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	# 创建input output窗体
	def _create_2_windows(self, width):
		cv2.namedWindow('input', cv2.WINDOW_NORMAL)
		cv2.resizeWindow('input', width, width)
		cv2.namedWindow('output', cv2.WINDOW_NORMAL)
		cv2.resizeWindow('output', width, width)
		
	def _show_all_windows(self):
		if cv2.waitKey(0) == 27:
			cv2.destroyAllWindows()
	
	# 在找到边缘前提下，获取最大面积的边缘
	def _get_contours_largest(self):
		area_largest = 0
		area_largest_cnt = []
		moments_largest = {}
		for cnt in self.contours:
			moments = cv2.moments(cnt)  # Calculate moments
			if moments['m00'] != 0:
				moment_area = moments['m00']  # Contour area from moment
				if area_largest < moment_area:
					area_largest = moment_area
					area_largest_cnt = cnt
					moments_largest = moments
		
		return (area_largest_cnt, moments_largest,)

	# 滑动Trackbar的回调函数，动态绘制不同canny阈值的边缘图像
	def _callback_draw_contours(self, thresh):
		# https://github.com/abidrahmank/OpenCV2-Python/blob/master/Official_Tutorial_Python_Codes/3_imgproc/moments.py
		self._find_contours(thresh)
		
		drawing = np.zeros(self.img.shape, np.uint8)  # Image to draw the contours
		for cnt in self.contours:
			moments = cv2.moments(cnt)  # Calculate moments
			if moments['m00'] != 0:
				cx = int(moments['m10'] / moments['m00'])  # cx = M10/M00
				cy = int(moments['m01'] / moments['m00'])  # cy = M01/M00
				moment_area = moments['m00']  # Contour area from moment
				print moment_area
				# contour_area = cv2.contourArea(cnt)             # Contour area using in_built function
				cv2.drawContours(drawing, [cnt], 0, 255, 1)  # draw contours 
				cv2.circle(drawing, (cx, cy), 3, 50, -1)  # draw centroids
		
		cv2.imshow('output', drawing)
		cv2.imshow('input', self.img)
		print '-' * 20
		
	# 带有滑动Trackbar的绘制边缘
	def draw_contours(self, thresh_max=None):
		if thresh_max is None:
			thresh_max = self.thresh_max
			
		# 添加一个属性可以调节窗口大小
		windows_width = 300
		self._create_2_windows(windows_width)
		
		cv2.namedWindow('bar', cv2.WINDOW_NORMAL)
		cv2.resizeWindow('bar', 400, 10)
		cv2.createTrackbar('canny_thresh:', 'bar', self.canny_thresh, thresh_max, self._callback_draw_contours)
		
		self._callback_draw_contours(self.canny_thresh)
		
		self._show_all_windows()

	# 绘制面积最大的边缘
	def draw_contours_largest(self):	
		self._find_contours(self.canny_thresh)
		cnt, moments = self._get_contours_largest()

		drawing = np.zeros(self.img.shape, np.uint8)  # Image to draw the contours
		cv2.drawContours(drawing, [cnt, ], 0, 255, 1)  # draw contours 
			
		# 添加一个属性可以调节窗口大小
		windows_width = 300
		self._create_2_windows(windows_width)
		cv2.imshow('output', drawing)
		cv2.imshow('input', self.img)
		self._show_all_windows()
		
	# 仅返回归一化的 Hu(1)，范围为0~1（手工截取)
	def get_humoments(self):
		self._find_contours(self.canny_thresh)
		cnt, moments = self._get_contours_largest()
		Hu_1 = cv2.HuMoments(moments)[0][0]
		if Hu_1 <= 0.0:return 0.0
		if Hu_1 >= 1.0:return 1.0
		return Hu_1
	
	# 返回一个剪裁后的图像，内容为正方形的前景，仅用于计算riLBP值（消除背景影响）
	def get_foreground(self):
		self._find_contours(self.canny_thresh)
		cnt, moments = self._get_contours_largest()
		(x, y), radius = cv2.minEnclosingCircle(cnt)
		x_center, y_center = x, y
		square=int(2*radius)
		x1, y1 = int(x_center - radius), int(y_center - radius)
		x2, y2 = x1+square,y1+square
		
		# 剪裁前景
		foreground = self.img[y1:y2, x1:x2]

		return foreground
		
if __name__ == '__main__':
# 	mypreprocess=my_Preprocess("../data/grains/heimi/1.jpg")
# 	cv2.namedWindow('bin',cv2.WINDOW_NORMAL)
# 	cv2.resizeWindow('bin', 300,300)
# 	myshape=my_SHAPE(mypreprocess.get_img_gray(),mypreprocess.get_img_binary())	
# 	img=myshape.get_foreground()
# 	cv2.imshow('i',mypreprocess.get_img_gray())
# 	cv2.imshow('bin',img)
# 	if cv2.waitKey(0) == 27:
# 		cv2.destroyAllWindows()
# 	sys.exit(0)
	
	prefix_name = "huangdou"
	for i in range(1, 11):
		mypreprocess = my_Preprocess("../data/grains/" + prefix_name +'/'+ str(i) + ".jpg", [48, 48])
		# cv2.imshow("bin",mypreprocess.get_img_binary())
		myshape = my_SHAPE(mypreprocess.get_img_gray())	
		# myshape.draw_contours()
		#myshape.draw_contours_largest()
		#print prefix_name, i, ":", '-' * 20
		print myshape.get_humoments()
		#print myshape.get_foreground()
