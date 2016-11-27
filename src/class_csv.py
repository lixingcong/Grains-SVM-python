#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月27日
@author: li
读取csv文件，获取文件列表
'''

import sys
import csv

class my_CSV(object):
	def __init__(self,csv_file):
		self.csv_file=csv_file
		
	def write(self,line,data):
		assert len(line) == len(data)
		with open(self.csv_file,'wb') as f:
			pass
		pass
	
	# line is start from index of 1
	def read(self,line,lines_to_read=1):
		with open(self.csv_file,'rb') as f:
			csv_reader = csv.reader(f, delimiter=',',quotechar='"')
			results=[]
			for i, row in enumerate(csv_reader):
				if i >= (line-1):
					results.append(row)
				if i == (line+lines_to_read-2):
					break
		return results if results != [] else None
	
	def insert(self,line,data):
		pass
	
	def delete(self,line):
		pass
	
if __name__ == '__main__':
	mycsv=my_CSV('/tmp/1.csv')
	print mycsv.read(2)
	
	