#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < demo_1.py 2016-11-23 17:08:41 >
"""
opencv基本灰度化处理
"""

import cv2
from matplotlib import pyplot as plt
import sys

img = cv2.imread("../data/4x3.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

ret,thresh1 = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
print img.shape
print img[0,2]
print len(img[0])
print len(img)
sys.exit(0)

cv2.imshow('image', thresh1)
cv2.waitKey(0)
cv2.destroyAllWindows()

# plt.figure("figure_111")
# plt.imshow(img, 'gray')
# plt.show()
