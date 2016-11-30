#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月26日
@author: li
获取归一化颜色分量，属于初级性能，没有太高的识别率容易受光线影响
归一化后只需要2个特征量，因为B=1-G-R
'''

import cv2
import numpy as np
from class_preprocess import my_Preprocess

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
	# print "#%02x%02x%02x" % (int(R), int(G), int(B))
	
	sum_BGR_last = B + G + R
	return (R / sum_BGR_last, G / sum_BGR_last, B / sum_BGR_last,)

# 线性标准化，返回list
def normalize_from_list(input_list):
	len_of_line = len(input_list[0])
	res = []
	for row in input_list:
		a1 = np.asarray(row, dtype=np.float64)
		a2 = np.zeros((len_of_line,), dtype=np.float64)
		# 标准化到[-1,+1]
		cv2.normalize(a1, a2, -1.0, 1.0, cv2.NORM_MINMAX)
		res.append(a2.tolist())
		
	return res
	
	
if __name__ == '__main__':
	# pic_prep = my_Preprocess("../data/s.png")
	# print get_rgb_normolized(pic_prep.get_img(), pic_prep.get_img_binary())
	
	a = [[1, 2, 3], [3, 4, 5], [6, 7, 8]]
	print normalize_from_list(a)
	
