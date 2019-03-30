
import numpy as np
import cv2
import math
import func_circle_detect as cdf
import time
#import line_profiler
import sys


img_name = "test_4.jpg"
img = cv2.imread(img_name)

gray = cv2.cvtColor(np.uint8(img),cv2.COLOR_BGR2GRAY)

gaussian_blur_para = 1
end_signal_hough = 0
while end_signal_hough == 0:
    hough_para2 = 10
    hough_para2_inc = 5
    end_signal_3 = 0
    old_num_circles = 1000
    

    while end_signal_3 == 0:
        circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,10,
                                param1=100, param2=hough_para2, minRadius=54, maxRadius=60)
        if hough_para2_inc < 0.0001:
            channel_ball_2 = cv2.GaussianBlur(gray,(0, 0),1)
            gaussian_blur_para = gaussian_blur_para + 1
            end_signal_3 = 1
        try:
            if len(circles[0]) > 1:
                hough_para2 = hough_para2 + hough_para2_inc
                if old_num_circles <=1:
                    hough_para2_inc = hough_para2_inc/2    
            if len(circles[0]) <= 1:
                hough_para2 = hough_para2 - hough_para2_inc
                if old_num_circles >=1:
                    hough_para2_inc = hough_para2_inc/2
            if (len(circles[0]) == 1) & (old_num_circles > 1) & (hough_para2_inc < 0.01):
                end_signal_3 = 1
                end_signal_hough =1
            old_num_circles = len(circles[0])
        except:
            hough_para2 = hough_para2 - hough_para2_inc
            hough_para2_inc = hough_para2_inc/2
            old_num_circles = 0
        if hough_para2 <= 0:
            hough_para2 = hough_para2 + hough_para2_inc +0.001
            hough_para2_inc = hough_para2_inc/2



x = circles[0][0][0]
y = circles[0][0][1]
r = circles[0][0][2]
print(x,y,r)
cv2.circle(img, (x,y), r, (0, 255, 0), 1, 1, 0)
#cv2.circle(img,(x,y), int(r-4), (0,0,0), -1)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# #######################################################################
# gray = cv2.cvtColor(np.uint8(img),cv2.COLOR_BGR2GRAY)


# gaussian_blur_para = 1
# end_signal_hough = 0
# while end_signal_hough == 0:
#     hough_para2 = 10
#     hough_para2_inc = 5
#     end_signal_3 = 0
#     old_num_circles = 1000
    

#     while end_signal_3 == 0:
#         circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,10,
#                                 param1=100, param2=hough_para2, minRadius=54, maxRadius=60)
#         if hough_para2_inc < 0.0001:
#             channel_ball_2 = cv2.GaussianBlur(gray,(0, 0),1)
#             gaussian_blur_para = gaussian_blur_para + 1
#             end_signal_3 = 1
#         try:
#             if len(circles[0]) > 1:
#                 hough_para2 = hough_para2 + hough_para2_inc
#                 if old_num_circles <=1:
#                     hough_para2_inc = hough_para2_inc/2    
#             if len(circles[0]) <= 1:
#                 hough_para2 = hough_para2 - hough_para2_inc
#                 if old_num_circles >=1:
#                     hough_para2_inc = hough_para2_inc/2
#             if (len(circles[0]) == 1) & (old_num_circles > 1) & (hough_para2_inc < 0.01):
#                 end_signal_3 = 1
#                 end_signal_hough =1
#             old_num_circles = len(circles[0])
#         except:
#             hough_para2 = hough_para2 - hough_para2_inc
#             hough_para2_inc = hough_para2_inc/2
#             old_num_circles = 0
#         if hough_para2 <= 0:
#             hough_para2 = hough_para2 + hough_para2_inc +0.001
#             hough_para2_inc = hough_para2_inc/2



# x = circles[0][0][0]
# y = circles[0][0][1]
# r = circles[0][0][2]
# print(x,y,r)
# cv2.circle(img, (x,y), r, (0, 255, 0), 1, 1, 0)
# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


 