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
	def __init__(self,input_gray,thresh=100):
		self.img=input_gray
		self.contours=None
		self.hierarchy=None
		self.thresh=thresh
		self.thresh_max=255
		self._find_contours(self.thresh)

	# 找出轮廓
	def _find_contours(self,thresh):
		edges = cv2.Canny(self.img,thresh,thresh*2)
		self.contours,self.hierarchy=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

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
				contour_area = cv2.contourArea(cnt)             # Contour area using in_built function
				cv2.drawContours(drawing,[cnt],0,127,1)   # draw contours 
				cv2.circle(drawing,(cx,cy),3,50,-1)      # draw centroids
		
		cv2.imshow('output',drawing)
		cv2.imshow('input',self.img)
		
	def draw_contours(self,thresh_max=None):
		if thresh_max is None:
			thresh_max=self.thresh_max
			
		# 添加一个属性可以调节窗口大小
		windows_width=300
		cv2.namedWindow('input',cv2.WINDOW_NORMAL)
		cv2.resizeWindow('input', windows_width,windows_width)
		cv2.namedWindow('output',cv2.WINDOW_NORMAL)
		cv2.resizeWindow('output', windows_width,windows_width)
		cv2.namedWindow('bar',cv2.WINDOW_NORMAL)
		cv2.resizeWindow('bar', 400,10)
		
		cv2.createTrackbar('canny thresh:','bar',self.thresh,thresh_max,self._callback_draw_contours)
		self._callback_draw_contours(self.thresh)
		if cv2.waitKey(0) == 27:
			cv2.destroyAllWindows()

	def get_moments(self):
		print self.contours


if __name__ == '__main__':
	mypreprocess=my_Preprocess("../data/s.png",[48,48])
	myshape=my_SHAPE(mypreprocess.get_img_gray())
	#myshape.get_moments()
	myshape.draw_contours()
