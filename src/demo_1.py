#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < demo_1.py 2016-11-23 17:08:41 >
"""
opencv基本灰度化处理
"""

import cv2
from matplotlib import pyplot as plt
import sys

img = cv2.imread("../data/s.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

img_resized = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
cv2.imwrite('../data/s_resized.png',img_resized)

img_resized=cv2.medianBlur(img_resized,1)
img_blur=cv2.bilateralFilter(img_resized,-1,20,20)

# ret,thresh1 = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)

cv2.imshow('image1', img_resized)
cv2.imshow('image2', img_blur)
# cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('../data/s_blur.png',img_blur)


# plt.figure("figure_111")
# plt.imshow(img, 'gray')
# plt.show()
