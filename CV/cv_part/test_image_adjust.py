import math
import time
import sys
from multiprocessing.pool import ThreadPool
import numpy as np
import argparse
import cv2



gamma = 1
saturation = 0.5

im = cv2.imread('test.jpg')

tic = time.time()

im = cv2.GaussianBlur(im, (0, 0), 5)
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

hsv_new = np.uint8(cv2.pow(hsv/255,saturation)*255)
hsv[:,:,1] = hsv_new[:,:,1]
im = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

toc = time.time() - tic
print("Time used: " + str(toc))

cv2.imshow('Original Image',im)
cv2.waitKey(0)


