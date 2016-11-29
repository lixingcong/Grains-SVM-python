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
		
	# data should be like this: [[2,3,4],[5,6,7],]
	# line is the index to write
	def write(self,data,line=None):	
		data_to_write=[]
		if line is not None:
			total_row_num=self.get_total_rows()
			rows_before=self.read(1,line-1)
			rows_after=self.read(line, total_row_num-line+1)
			data_to_write=self._merge_3_data(rows_before, data, rows_after)
		else:
			data_to_write=data
			
		with open(self.csv_file,'wb') as f:
			csv_writer=csv.writer(f, delimiter=',',quotechar='"')
			csv_writer.writerows(data_to_write)
	
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
	
	def _merge_3_data(self,d1,d2,d3):
		res=[]
		for i in d1:res.append(i)				
		for i in d2:res.append(i)				
		for i in d3:res.append(i)
		return res
	
	def get_total_rows(self):
		with open(self.csv_file,'rb') as f:
			csv_reader = csv.reader(f, delimiter=',',quotechar='"')
			return len(zip(enumerate(csv_reader)))
			
		
if __name__ == '__main__':
	mycsv=my_CSV('/tmp/1.csv')
# 	print mycsv.read(2)
# 	print mycsv.get_total_rows()
	mycsv.write([[3234,54324,534],[23334,6573,5685684]])
	
	