#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/lionaneesh/LBP-opencv-python/blob/master/Uniform-Circular-LBP.py

# 该文件不能作为算法使用，仅供注释理解LBP工作过程

import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

img_file = '../data/3x3.png'
cir_min_sum_dict={}

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

# 找出跳变次数（用于Uniform Pattern）
def find_variations(pixel_values):
    prev = pixel_values[-1] # 最后一个元素
    t = 0
    for p in range(0, len(pixel_values)):
        cur = pixel_values[p]
        if cur != prev:
            t += 1
        prev = cur
    return t
   
# 计算一个二进制列表的对应十进制值
def get_hex_sum(input_list):
	res = 0
	len_ = len(input_list)
	for i in range(len_):
		res += (input_list[i] << (i)) # 数据存储方式：低位在list前面
	return res

# 循环LBP的最小值
def get_cir_min_value(input_list):
	len_ = len(input_list)
	cir_min_sum = get_hex_sum(input_list)
	# print cir_min_sum
	for i in range(1, len_):
		last_element = input_list.pop(len_ - 1)
		input_list.insert(0, last_element)
		this_sum = get_hex_sum(input_list)
		# print this_sum
		if this_sum < cir_min_sum:
			cir_min_sum = this_sum
	return cir_min_sum

# 生成一个Look up table，参数P为LBP周围采样点的个数
def gen_cir_min_sum_dict(P):
	global cir_min_sum_dict
	max_val = 1 << P
	for i in range(max_val):
		bits = []
		for bit in range(P):
			bits.append((i & (1 << bit)) >> bit) # 数据存储方式：低位排在list前面

		cir_min_sum_dict[i] = get_cir_min_value(bits)
		
def get_cir_lbp_val(sum_value):
	return cir_min_sum_dict[sum_value]

img = cv2.imread(img_file, 0)
transformed_img = cv2.imread(img_file, 0)
unassigned = []
pixel_values = set()

P = 8  # number of pixels ps：当8像素时候，Uniform对应有57种Uniform值，其余归类为第58类，实现直方图256维降维到58维
R = 1  # radius 

no_of_pixel_values = 0

def calc_lbp():
	global pixel_values, no_of_pixel_values, unassigned
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
	        # 为了解决二进制模式过多的问题，提高统计性，Ojala提出了采用
	        # 一种“等价模式”（Uniform Pattern）来对LBP算子的模式种类进行降维。
	        # 即：绝大多数LBP模式最多只包含两次从1到0或从0到1的跳变
	        variations = find_variations(values)
	        res=255
	        if variations <= 2:
	            res = 0
	            bits_sum=get_hex_sum(values)
	            res=get_cir_lbp_val(bits_sum)
	            transformed_img.itemset((x, y), res)
	            pixel_values.add(res)
	        else:
	            unassigned.append((x, y))
	        
	        print "(%d,%d): res=%d"%(x,y,res)
	
	unassigned_value = len(pixel_values)
	pixel_values = sorted(pixel_values)
	no_of_pixel_values = len(pixel_values)
	
	# 使用一个字典实现list的逆向映射val->p，目的是绘制transform_img图片
	trans_p1_u2 = {}
	for p in range(0, len(pixel_values)):
	    trans_p1_u2[pixel_values[p]] = p
	
	for r in range(0, len(transformed_img)):
	    for c in range(0, len(transformed_img[0])):
	        if (r, c) in unassigned:
	            transformed_img.itemset((r, c), unassigned_value)
	        else:
	            p1 = transformed_img[(r, c)]
	            transformed_img.itemset((r, c), trans_p1_u2[p1])
    
def show_plot():
# 	cv2.imshow('image', img)
# 	cv2.imshow('thresholded image', transformed_img)
	
	# histogram参数：第一个是输入值，第二个是对应坐标(刻度可变的坐标)，第三个是y刻度最大值
	hist, bins = np.histogram(transformed_img.flatten(), no_of_pixel_values + 1, [0, no_of_pixel_values])
	
	# cumsum:返回一个累加和（概率密度分布曲线）
	cdf = hist.cumsum()
	cdf_normalized = cdf * hist.max() / cdf.max()
	
# 	plt.plot(cdf_normalized, color='b')
# 	plt.show()
	plt.hist(transformed_img.flatten(), no_of_pixel_values, [0, no_of_pixel_values], color='b')
	plt.xlim([0, no_of_pixel_values])
	plt.legend(('cdf', 'histogram'), loc='upper left')
	plt.show()
	
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == '__main__':
	gen_cir_min_sum_dict(P)
	calc_lbp()
	show_plot()
