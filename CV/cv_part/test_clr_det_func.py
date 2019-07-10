# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 20:40:57 2018

@author: 75678
"""

import cv2
import math
import func_circle_detect as cdf
import time
# import line_profiler
import sys


#img_name = "1547272570.814634.jpg"
#img_name = "2_1.jpg"
img_name = "test.jpg"
img = cv2.imread(img_name)

tic = time.time()
for i in range(0,1):
    img = cv2.imread(img_name)
    circle_centers, circle_radius, out_put_img = cdf.circle_center_detect_single_ball (img, 1, 
                                                                                    [40.0,30.35,43.4], [77.69,82.13,78.1], 
                                                                                    [0,0,0], 0, 3, 
                                                                                    0, [0,0,0], [0,0,0])
#    circle_centers, circle_radius, out_put_img = cdf.circle_center_detect(img, 1,50,100,40)
toc = time.time() - tic
print("Running for 20 frames")
print("Min radius: 0, Max Radius 100")
print("Time used: " + str(toc))
#print("circle_center:" + str(circle_centers[0]) + " , " + str(circle_centers[1]))

#cv2.imwrite("out_put" + img_name, out_put_img)

print(circle_centers)
print(circle_radius)

#img_name = "1547272570.814634.jpg"
#img = cv2.imread(img_name)
#
#circle_centers, circle_radius, out_put_img = cdf.circle_center_detect (img, 0, 0 , 0)
#
#cv2.imwrite("out_put" + img_name, out_put_img)

#cv2.imshow("show",out_put_img)
#cv2.imshow("show",gray)
#cv2.waitKey(0)
#cv2.destroyAllWindows() 

#print(circle_centers)


 # constant defination

