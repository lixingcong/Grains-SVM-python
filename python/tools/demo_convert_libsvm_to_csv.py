#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年12月2日
@author: li
将libsvm专用的训练样本文件转成csv文件
'''

filename_test_txt="/tmp/s1.txt"
filename_train_txt="/tmp/s2.txt"

filename_test_csv='../data/test_features_cross_validation.csv'
filename_train_csv='../data/grain_features_cross_validation.csv'

def parse_train_txt(input_txt,output_csv):
	with open(input_txt,"r") as f_in:
		with open(output_csv,"w") as f_out:
			for line in f_in:
				line_split=line.split(" ")
				f_out.write("Chinese-"+line_split[0]+",")
				f_out.write(line_split[0]+",")
				for x in line_split[1:]:
					x_splited=x.split(":")
					if len(x_splited)==2 and x_splited[1]!="":
						f_out.write(x_splited[1]+",")
			
				f_out.write('\n');

if __name__ == '__main__':
	parse_train_txt(filename_test_txt,filename_test_csv)
	parse_train_txt(filename_train_txt,filename_train_csv)