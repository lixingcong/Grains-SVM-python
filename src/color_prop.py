#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月26日
@author: li
获取归一化颜色分量，属于初级性能，没有太高的识别率容易受光线影响
'''

import cv2
import numpy as np
from class_preprocess import myPreprocess

# 输入彩色和二值化图像即可
def get_rgb_normolized(input_img, input_img_bin):
	total_valid_pixels = 0
	sum_BGR = [0, 0, 0, ]  # 分别是BGR
	height, width = input_img_bin.shape
	
	# 遍历像素
	for y in range(height):
		for x in range(width):
			if input_img_bin[y, x] > 0:
				total_valid_pixels += 1
				sum_BGR[0] += input_img[y, x, 0]  # B
				sum_BGR[1] += input_img[y, x, 1]  # G
				sum_BGR[2] += input_img[y, x, 2]  # R
	
	# 归一化
	BGR = [x / total_valid_pixels for x in sum_BGR]
	B, G, R = float(BGR[0]), float(BGR[1]), float(BGR[2])

	# Web 配色预览
	print "#%02x%02x%02x" % (int(R), int(G), int(B))
	
	sum_BGR_last = B + G + R
	return (R / sum_BGR_last, G / sum_BGR_last, B / sum_BGR_last,)
	
if __name__ == '__main__':
	pic_prep = myPreprocess("../data/s.png")
	print get_rgb_normolized(pic_prep.get_img(), pic_prep.get_img_binary())
