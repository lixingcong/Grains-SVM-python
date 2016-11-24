#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/lionaneesh/LBP-opencv-python/blob/master/Uniform-Circular-LBP.py

# 已经将uLBP重写为riLBP

import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

img_file = '../data/3x3.png'
dict_sum_to_rilbp={}

# 双线性插值（用于旋转）
def bilinear_interpolation(x, y, img):
    x1, y1 = int(x), int(y)
    x2, y2 = math.ceil(x), math.ceil(y)

    r1 = (x2 - x) / (x2 - x1) * get_pixel_else_0(img, x1, y1) + (x - x1) / (x2 - x1) * get_pixel_else_0(img, x2, y1)
    r2 = (x2 - x) / (x2 - x1) * get_pixel_else_0(img, x1, y2) + (x - x1) / (x2 - x1) * get_pixel_else_0(img, x2, y2)

    return (y2 - y) / (y2 - y1) * r1 + (y - y1) / (y2 - y1) * r2    

# 求pixels中元素相对于center的阈值
def thresholded(center, pixels):
    out = []
    for a in pixels:
        if a >= center:
            out.append(1)
        else:
            out.append(0)
    return out

# 获取图片中任意一点(index_x, index_y)，无效值返回0
def get_pixel_else_0(image, idx, idy):
    if idx < int(len(image)) - 1 and idy < len(image[0]):
        return image[idx, idy]
    else:
        return 0
   
# 计算一个二进制列表的对应十进制值
def get_sum_from_bin(input_list):
	res = 0
	len_ = len(input_list)
	for i in range(len_):
		res += (input_list[i] << (i)) # 数据存储方式：低位在list前面
	return res

# 循环不变LBP的最小值
def get_rilbp_from_bin(input_list):
	len_ = len(input_list)
	min_lbp = get_sum_from_bin(input_list)
	# print min_lbp
	for i in range(1, len_):
		last_element = input_list.pop(len_ - 1)
		input_list.insert(0, last_element)
		this_sum = get_sum_from_bin(input_list)
		# print this_sum
		if this_sum < min_lbp:
			min_lbp = this_sum
	return min_lbp

# 生成一个Look up table，参数P为LBP周围采样点的个数
def gen_dict_sum_to_rilbp(sample_num):
	global dict_sum_to_rilbp
	max_val = 1 << sample_num
	for i in range(max_val):
		bits = []
		for bit in range(sample_num):
			bits.append((i & (1 << bit)) >> bit) # 数据存储方式：低位排在list前面

		dict_sum_to_rilbp[i] = get_rilbp_from_bin(bits)

def gen_dict_rilbp_to_histogram_x():
	global dict_sum_to_rilbp
	pass
		
def get_rilbp_from_sum(sum_value):
	return dict_sum_to_rilbp[sum_value]

img = cv2.imread(img_file, 0)
transformed_img = cv2.imread(img_file, 0)

P = 8  # number of pixels ps：当8像素时候，Uniform对应有57种Uniform值，其余归类为第58类，实现直方图256维降维到58维
R = 1  # radius 

no_of_pixel_values = 0

def calc_lbp():
	global no_of_pixel_values, unassigned
	for x in range(0, len(img)):
	    for y in range(0, len(img[0])):
	        center = img[x, y]
	        pixels = []
	        for point in range(1, P + 1):
	            r = x + R * math.cos(2 * math.pi * point / P)
	            c = y - R * math.sin(2 * math.pi * point / P)
	            if r < 0 or c < 0:
	                pixels.append(0)
	                continue            
	            if int(r) == r:
	                if int(c) != c:
	                    c1 = int(c)
	                    c2 = math.ceil(c)
	                    w1 = (c2 - c) / (c2 - c1)
	                    w2 = (c - c1) / (c2 - c1)
	                    # 插值
	                    pixels.append(int((w1 * get_pixel_else_0(img, int(r), int(c)) + \
	                                   w2 * get_pixel_else_0(img, int(r), math.ceil(c))) / (w1 + w2)))
	                else:
	                	# 双线性插值
	                    pixels.append(get_pixel_else_0(img, int(r), int(c)))
	            elif int(c) == c:
	                r1 = int(r)
	                r2 = math.ceil(r)
	                w1 = (r2 - r) / (r2 - r1)
	                w2 = (r - r1) / (r2 - r1)                
	                pixels.append((w1 * get_pixel_else_0(img, int(r), int(c)) + \
	                               w2 * get_pixel_else_0(img, math.ceil(r), int(c))) / (w1 + w2))
	            else:
	                pixels.append(bilinear_interpolation(r, c, img))
		
	        values = thresholded(center, pixels)

            bits_sum=get_sum_from_bin(values)
            res=get_rilbp_from_sum(bits_sum)
            transformed_img.itemset((x, y), res)
            
            print "(%d,%d): res=%d"%(x,y,res)
	
    
def show_plot():
# 	cv2.imshow('image', img)
# 	cv2.imshow('thresholded image', transformed_img)
	
	# histogram参数：第一个是输入值，第二个是对应坐标(刻度可变的坐标)，第三个是y刻度最大值
	hist, bins = np.histogram(transformed_img.flatten())
	
	# cumsum:返回一个累加和（概率密度分布曲线）
	cdf = hist.cumsum()
	cdf_normalized = cdf * hist.max() / cdf.max()
	
# 	plt.plot(cdf_normalized, color='b')
# 	plt.show()
	plt.hist(transformed_img.flatten(), color='b')
# 	plt.xlim([0, no_of_pixel_values])
	plt.legend(('cdf', 'histogram'), loc='upper left')
	plt.show()
	
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == '__main__':
	gen_dict_sum_to_rilbp(P)
	calc_lbp()
	show_plot()
