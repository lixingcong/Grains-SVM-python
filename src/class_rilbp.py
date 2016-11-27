#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月25日
@author: li
Rotation invariant Local Binary Pattern（旋转不变的局部二值化模式）
'''
import cv2
from matplotlib import pyplot as plt
import math

class my_RILBP(object):
	def __init__(self, radius=1, neighbors=8):
		self.img_height = 0
		self.img_width = 0
		self.img = None
		
		self.lbp_radius = radius
		self.lbp_neighbors = neighbors  # 邻居采样点数
		
		self.dict_sum_to_rilbp = {}
		self.dict_rilbp_to_histogram_x = {}
		
		self.histogram_x_width = 0
		self.histogram_result = []
		self._gen_dict_sum_to_rilbp()
		self._gen_dict_rilbp_to_histogram_x()
		
	# 生成一个Look up table，参数P为LBP周围采样点的个数
	def _gen_dict_sum_to_rilbp(self):
		max_val = 1 << self.lbp_neighbors
		for i in range(max_val):
			bits = []
			for bit in range(self.lbp_neighbors):
				bits.append((i & (1 << bit)) >> bit)  # 数据存储方式：低位排在list前面
	
			self.dict_sum_to_rilbp[i] = self._get_rilbp_from_bin(bits)

	# 生成一个Look up table 将riLBP的所有值映射到直方图的横坐标
	def _gen_dict_rilbp_to_histogram_x(self):
		set_rilbp = set()
		for key in self.dict_sum_to_rilbp:
			set_rilbp.add(self.dict_sum_to_rilbp[key])
	
		self.dict_rilbp_to_histogram_x = {}
		index = 0
		for rilbp in sorted(set_rilbp):
			self.dict_rilbp_to_histogram_x[rilbp] = index
			index += 1
	
		self.histogram_x_width = index
		self.histogram_result = [0] * self.histogram_x_width
	
	# 双线性插值（用于旋转后的像素插值）
	def _bilinear_interpolation(self, x, y):
		x1, y1 = int(x), int(y)
		x2, y2 = math.ceil(x), math.ceil(y)
	
		r1 = (x2 - x) / (x2 - x1) * self._get_pixel_else_0(x1, y1) + (x - x1) / (x2 - x1) * self._get_pixel_else_0(x2, y1)
		r2 = (x2 - x) / (x2 - x1) * self._get_pixel_else_0(x1, y2) + (x - x1) / (x2 - x1) * self._get_pixel_else_0(x2, y2)
	
		return (y2 - y) / (y2 - y1) * r1 + (y - y1) / (y2 - y1) * r2
	
	# 获取图片中任意一点(index_x, index_y)，无效值返回0
	# 注意：opencv中img[y,x]对应于图像处理规范坐标的img[x,y]
	def _get_pixel_else_0(self, idx, idy):
		x, y = int(idx), int(idy)
		if x < self.img_width and y < self.img_height:
			return self.img[y, x]
		else:
			return 0
		
	# 求pixels(列表)中元素相对于center的阈值
	def _thresholded(self, center, pixels):
		out = []
		for a in pixels:
			if a >= center:
				out.append(1)
			else:
				out.append(0)
		return out
			
	# 计算一个二进制列表的对应十进制值
	def _get_sum_from_bin(self, input_list):
		res = 0
		len_ = len(input_list)
		for i in range(len_):
			res += (input_list[i] << (i))  # 数据存储方式：低位在list前面
		return res
	
	# 循环不变LBP的最小值
	def _get_rilbp_from_bin(self, input_list):
		len_ = len(input_list)
		min_lbp = self._get_sum_from_bin(input_list)
		for i in range(1, len_):
			last_element = input_list.pop(len_ - 1)
			input_list.insert(0, last_element)
			this_sum = self._get_sum_from_bin(input_list)
			if this_sum < min_lbp:
				min_lbp = this_sum
		return min_lbp
	
	# 返回一个直方图，list类型
	def get_lbp_histogram(self, input_img):
		self.img_height = input_img.shape[0]
		self.img_width = input_img.shape[1]
		if len(input_img.shape) > 2:
			self.img = cv2.cvtColor(input_img, cv2.COLOR_RGB2GRAY)
		else:
			self.img = input_img

		# initialize result
		for i in range(len(self.histogram_result)):
			self.histogram_result[i]=0

		# 遍历像素
		for x in range(self.img_width):
			for y in range(self.img_height):
				center = self._get_pixel_else_0(x, y)
				pixels = []  # 邻居像素列表
				for point in range(1, self.lbp_neighbors + 1):
					r = x + self.lbp_radius * math.cos(2 * math.pi * point / self.lbp_neighbors)  # x
					c = y - self.lbp_radius * math.sin(2 * math.pi * point / self.lbp_neighbors)  # y
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
							pixels.append(int((w1 * self._get_pixel_else_0(int(r), int(c)) + \
										   w2 * self._get_pixel_else_0(int(r), math.ceil(c))) / (w1 + w2)))
						else:
							# 双线性插值
							pixels.append(self._get_pixel_else_0(int(r), int(c)))
					elif int(c) == c:
						r1 = int(r)
						r2 = math.ceil(r)
						w1 = (r2 - r) / (r2 - r1)
						w2 = (r - r1) / (r2 - r1)
						pixels.append((w1 * self._get_pixel_else_0(int(r), int(c)) + \
									   w2 * self._get_pixel_else_0(math.ceil(r), int(c))) / (w1 + w2))
					else:
						pixels.append(self._bilinear_interpolation(r, c))
	
				values = self._thresholded(center, pixels)
	
				rilbp = self._get_rilbp_from_bin(values)
				histogram_x = self.dict_rilbp_to_histogram_x[rilbp]
				self.histogram_result[histogram_x] += 1
				# print "(%d,%d): rilbp=%d, histogram_x=%d"%(x,y,rilbp,histogram_x)
	
		# 归一化
		histogram_y_sum=0
		for histogram_y in self.histogram_result:
			histogram_y_sum+=histogram_y
			
		return [float(x) / histogram_y_sum for x in self.histogram_result]

	def get_histogram_x_width(self):
		return self.histogram_x_width
	
if __name__ == '__main__':
	img_file = '../data/yundou-1.png'
	img = cv2.imread(img_file, 0)
	img = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
	
	# LBP
	my_rilbp = my_RILBP(radius=1, neighbors=8)
	histogram_result = my_rilbp.get_lbp_histogram(img)
	print histogram_result
	
	# plot bar
	x = range(len(histogram_result))
	y = histogram_result
	plt.bar(x, y, color='r')
	plt.title("histogram")
	plt.show()
