# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 16:36:11 2018

@author: Haonan
"""
import cv2
import math
import numpy as np
import time
import sys

class circle_temp_class:
    center = None
    radius = None
    color_vec = np.array([0,0,0])

# return class of the function: circle_center_detect, contains the center of the three color circles [B, G, R]
class circle_class:
    b = np.array([0,0])
    g = np.array([0,0])
    r = np.array([0,0])

def circle_center_detect (img, showplot, circle_radius_min, circle_radius_max, min_center_distance):
    
    # constant defination
    pi = math.pi
    color_detect3_threshhold = 20
    sample_number = 30
    
    circle_radius_min = int(circle_radius_min)
    circle_radius_max = int(circle_radius_max)

    gaussian_blur_para = 2
    
    circle_temp = [circle_temp_class(), circle_temp_class(), circle_temp_class()]
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #Gaussian filter
    
    #cv2.imshow("show",gray)
    #cv2.waitKey(0)
    
    # denoise
    img = cv2.GaussianBlur(img, (0,0), 4)
    end_signal_hough = 0
    while end_signal_hough == 0:
        gray = cv2.GaussianBlur(gray,(0, 0),gaussian_blur_para)
        hough_para2 = 10
        circles = np.zeros((2,2))
        hough_para2_inc = 5
        end_signal_3 = 0
        old_num_circles = 1000
        #circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,2.0,30)
        if gaussian_blur_para >=5:
            print("[ERROR]:Hough circle detect failed")
            return -1
    
        while end_signal_3 == 0:
            circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,min_center_distance,
                                   param1=100, param2=hough_para2, minRadius=circle_radius_min, maxRadius=circle_radius_max)
            if hough_para2_inc < 0.0000001:
                end_signal_3 = 1
                gaussian_blur_para = gaussian_blur_para + 1
                #print("[IMG]:Gaussian blur parameter increased")
            try:
                if len(circles[0]) > 3:
                    hough_para2 = hough_para2 + hough_para2_inc
                    if old_num_circles <=3:
                        hough_para2_inc = hough_para2_inc/2    
                if len(circles[0]) <= 3:
                    hough_para2 = hough_para2 - hough_para2_inc
                    if old_num_circles >=3:
                        hough_para2_inc = hough_para2_inc/2
                if (len(circles[0]) == 3) & (old_num_circles > 3) & (hough_para2_inc < 0.1):
                    end_signal_3 = 1
                    end_signal_hough =1
                old_num_circles = len(circles[0])
            except:
                hough_para2 = hough_para2 - hough_para2_inc
                hough_para2_inc = hough_para2_inc/2
                old_num_circles = 0        
        
    for i in circles:
        counter=0
        for j in i: #extract center and radius of the three circles
            circle_temp[counter].center = (j[0], j[1])
            circle_temp[counter].radius = j[2]
           
            # draw center
            #cv2.circle(img, circle_temp[counter].center, 3, (0, 255, 0), -1, 8, 0)
            # 绘制圆轮廓
            cv2.circle(img, circle_temp[counter].center, circle_temp[counter].radius, (255, 255, 255), 1, 1, 0)
                
            #sample points to detect color
            for k in range(0, sample_number):
                pointX = int(round(circle_temp[counter].center[0] + 0.8*circle_temp[counter].radius * np.sin (2*k*pi/sample_number)))
                pointY = int(round(circle_temp[counter].center[1] + 0.8*circle_temp[counter].radius * np.cos (2*k*pi/sample_number)))
                pointColor = img[pointY, pointX]  # [IMPORTANT] Notice that in the index, x and y are reversed
                #detected_color = color_detect(pointColor, blue_ref, green_ref, red_ref, ref_threshhold)
                detected_color = color_detect4(pointColor, color_detect3_threshhold)
                
                draw_color = img[pointY, pointX]
                if np.sum(detected_color) > 1:
                    draw_color = np.array((255,255,255))
                elif np.sum(detected_color) == 0:
                    draw_color = np.array((0,0,0))
                draw_color = (float(draw_color[0]),float(draw_color[1]),float(draw_color[2]))
                
                circle_temp[counter].color_vec = circle_temp[counter].color_vec + detected_color
                cv2.circle(img, (pointX, pointY), 1, draw_color, 1, 1, 0)
                
            counter = counter + 1
    
    # Color assign         
    end_signal = 0    
    counter2 = 0
    filter1 = np.array([1, 1, 1])
    booled_color_vec = [np.array([0,0,0]), np.array([0,0,0]), np.array([0,0,0])]
    booled_color_vec[0] = boolize(circle_temp[0].color_vec)
    booled_color_vec[1] = boolize(circle_temp[1].color_vec)
    booled_color_vec[2] = boolize(circle_temp[2].color_vec)
    
    circle_centers = np.zeros((3,2))
    circle_radius = np.zeros(3)

        
    if showplot == 1:        
        cv2.imshow("img",img)
        #cv2.imshow("show",gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
    
    while end_signal != 1:
        if sum(filter1 * booled_color_vec[counter2 % 3]) != 1:
            counter2 = counter2 + 1
            if counter2 > 50:
                print("[ERROR]:Color assign failed, the can be because the colors are confusing, please check the threshold of the color dectect function")
                return np.zeros((3, 2)), np.zeros(3), img
            continue
        else:
            if (filter1 *booled_color_vec[counter2 % 3])[0] == 1: #The circle is blue
                circle_centers[0] = circle_temp[counter2 % 3].center
                circle_radius[0] = circle_temp[counter2 % 3].radius
                filter1 = filter1 - filter1 * booled_color_vec[counter2 % 3]
            elif (filter1 *booled_color_vec[counter2 % 3])[1] == 1:
                circle_centers[1] = circle_temp[counter2 % 3].center
                circle_radius[1] = circle_temp[counter2 % 3].radius
                filter1 = filter1 - filter1 * booled_color_vec[counter2 % 3]
            elif (filter1 *booled_color_vec[counter2 % 3])[2] == 1:
                circle_centers[2] = circle_temp[counter2 % 3].center
                circle_radius[2] = circle_temp[counter2 % 3].radius
                filter1 = filter1 - filter1 * booled_color_vec[counter2 % 3]
            else:
                print("[ERROR] color assign failed")
        if np.sum(filter1) == 0:
            end_signal = 1
        if counter2 > 50:
            print("[ERROR]:Color assign failed, the can be because the colors are confusing, please check the threshold of the color dectect function")
            return np.zeros((3, 2)), np.zeros(3), img
        counter2 = counter2 + 1      

    cv2.circle(img, (int(circle_centers[0][0]),int(circle_centers[0][1])), 1, (255, 50, 50), 1, 1, 0)
    cv2.circle(img, (int(circle_centers[1][0]),int(circle_centers[1][1])), 1, (50, 255, 50), 1, 1, 0)
    cv2.circle(img, (int(circle_centers[2][0]),int(circle_centers[2][1])), 1, (0, 0, 0), 1, 1, 0)
    
    #cv2.imwrite("out_put_img.jpg",img)    
    if showplot == 1:        
        cv2.imshow("show",img)
        #cv2.imshow("show",gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
    return circle_centers, circle_radius, img
        
# Description: Detect color of the point and return an array [blue, green, red, gray] if the position is 1
# Input: all 1X3 array-like        

    
def color_detect4 (target_color, threshhold):
    color = np.array((0,0,0))
    b = int(target_color[0])
    g = int(target_color[1])
    r = int(target_color[2])
    
    # green 
    if ((b-r)>(-10)) & ((g-r)>30) & ((g-b)>15):
        color[0] = 1
    # yellow    
    if (abs(r-g)<40) & ((r-b)>20) & ((g-b)>30):
        color[1] = 1
    # red     
    if ((r-g)>70) & ((r-b)>15) & ((b-g)>25):
        color[2] = 1
    
    return color

# boolize function, takes array as input, and output a same sized array with only 0 or 1    
def boolize (arr):
    for i in range(0, len(arr)):
        if arr[i] == 0:
            arr[i] = 0
        else:
            arr[i] = 1
    return arr


