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

def circle_center_detect_single_ball (img, showplot, circle_radius_min, circle_radius_max, ref_color, num_ball, idx_cam):
    img_origin = img
    # constant defination
    pi = math.pi
    color_detect3_threshhold = 20
    sample_number = 30
    
    circle_radius_min = np.int_(circle_radius_min)
    circle_radius_max = np.int_(circle_radius_max)


    
    circle_temp = [circle_temp_class(), circle_temp_class(), circle_temp_class()]
    
    
###############################################

    h, w = img.shape[:2]
    
    img = cv2.GaussianBlur(img, (0,0), 1)

    red = np.float32(img[:,:,2])
    green = np.float32(img[:,:,1])
    blue = np.float32(img[:,:,0])   

# Old channel method ----------------------------------------------------------------------------------
    
    if (idx_cam == 0)or(idx_cam==1):
        channel_ball_2 = np.uint8((3*(red-green)).clip(min=0,max=255)) # red
        channel_ball_0 = np.uint8((3*(green-red)).clip(min=0,max=255)) # green
        channel_ball_1 = np.uint8((2*((red-blue)).clip(min=0,max=255)-channel_ball_2).clip(min=0,max=255))  # yellow
    if (idx_cam == 2)or(idx_cam==3):
        channel_ball_2 = np.uint8((3*(red-green)).clip(min=0,max=255)) # red
        channel_ball_0 = np.uint8((3*(green-red)).clip(min=0,max=255)) # green
        channel_ball_1 = np.uint8((2*((red-blue)).clip(min=0,max=255)-channel_ball_2).clip(min=0,max=255))  # yellow
    
    # channel_ball_2_temp = (7*(red-green)).clip(min=0,max=255) # red
    # channel_ball_0_temp = (7*(green-red)).clip(min=0,max=255) # green
    # channel_ball_1_temp = (7*((red-blue)).clip(min=0,max=255)-channel_ball_0_temp).clip(min=0,max=255)  # yellow

    # channel_ball_0 = np.uint8((channel_ball_0_temp - channel_ball_1_temp - channel_ball_2_temp).clip(min=0,max=255))
    # channel_ball_1 = np.uint8((channel_ball_1_temp - channel_ball_0_temp - channel_ball_2_temp).clip(min=0,max=255))
    # channel_ball_2 = np.uint8((channel_ball_2_temp - channel_ball_0_temp - channel_ball_1_temp).clip(min=0,max=255))


    if showplot == 1:
        cv2.imshow("green",channel_ball_0)
        cv2.imshow("yellow",channel_ball_1)
        cv2.imshow("red",channel_ball_2)
        #cv2.imshow("show",gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
# Old channel method ----------------------------------------------------------------------------------
    
##    ref_color = np.array([[210,230,135],[90,250,230],[250,80,190]]) # green, yellow, red 
#    ref_color = np.array([[30,180,20],[60,120,170],[100,60,160]])
#
#    num_ball = 3
#    channel = np.zeros((h,w,num_ball))
#    
#    for idx_ball in range(num_ball):
#        d_r = np.absolute(np.ones((h,w))*ref_color[idx_ball,2]-img[:,:,2])
#        d_g = np.absolute(np.ones((h,w))*ref_color[idx_ball,1]-img[:,:,1])
#        d_b = np.absolute(np.ones((h,w))*ref_color[idx_ball,0]-img[:,:,0])
#        
##        d_r = np.square(d_r)
##        d_g = np.square(d_g)
##        d_b = np.square(d_b)
#        channel[:,:,idx_ball] = (np.ones((h,w))*255-(d_r+d_g+d_b)).clip(min=0)
#        
#    
#    #cv2.imshow("show",np.uint8(channel[:,:,1])) 
#    #cv2.waitKey(0)
#    #cv2.destroyAllWindows() 
#    
#    channel_new = np.zeros((h,w,num_ball))
#    for idx_ball in range(num_ball):
#        list_remain = list(range(num_ball))
#        list_remain.remove(idx_ball)
#        print(list_remain)
#        channel_remain_sum = np.zeros((h,w))
#        for i in range(len(list_remain)):
#            idx_ball_2 = list_remain[i]
#            channel_remain_sum += channel[:,:,idx_ball_2]
#        channel_remain_avg = channel_remain_sum/len(list_remain)
#        channel_new[:,:,idx_ball] = np.uint8((channel[:,:,idx_ball]-channel_remain_avg).clip(min=0))
#    channel_ball_0 = np.uint8(channel_new[:,:,0])
#    channel_ball_1 = np.uint8(channel_new[:,:,1])
#    channel_ball_2 = np.uint8(channel_new[:,:,2])
#    
#    if showplot ==1:
#        cv2.imshow("ball0",channel_ball_0)
#        cv2.imshow("ball1",channel_ball_1)
#        cv2.imshow("ball2",channel_ball_2)
#        #cv2.imshow("show",gray)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows() 

###############################################

#    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    # denoise for color image
    img = cv2.GaussianBlur(img, (0,0), 4)
    
    circles_info = np.zeros([1,3,3]) # Initialize circles
    
    # Ball 0 channel-----------------------------------------------------------
    gaussian_blur_para = 1
    end_signal_hough = 0
    while end_signal_hough == 0:
        
        hough_para2 = 10
        hough_para2_inc = 5
        end_signal_3 = 0
        old_num_circles = 1000
        
        if gaussian_blur_para >=5:
            print("[ERROR]:Hough circle detect failed")
            return -1
    
        while end_signal_3 == 0:
            circles = cv2.HoughCircles(channel_ball_0,cv2.HOUGH_GRADIENT,1,10,
                                   param1=100, param2=hough_para2, minRadius=circle_radius_min[0], maxRadius=circle_radius_max[0])
            if hough_para2_inc < 0.0001:
                channel_ball_0 = cv2.GaussianBlur(channel_ball_0,(0, 0),1)
                gaussian_blur_para = gaussian_blur_para + 1
                end_signal_3 = 1
                print("[IMG]:Gaussian blur parameter increased")
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
            if showplot == 1:
                print("Ball0: Current Hough para2 = " + str(hough_para2))
    circles_info[0][0] = circles[0][0] 
                
    # Ball 1 channel-----------------------------------------------------------
    gaussian_blur_para = 1
    end_signal_hough = 0
    while end_signal_hough == 0:
        hough_para2 = 10
        hough_para2_inc = 5
        end_signal_3 = 0
        old_num_circles = 1000
        
        if gaussian_blur_para >=5:
            
            print("[ERROR]:Hough circle detect failed")
            return -1
    
        while end_signal_3 == 0:
            circles = cv2.HoughCircles(channel_ball_1,cv2.HOUGH_GRADIENT,1,10,
                                   param1=100, param2=hough_para2, minRadius=circle_radius_min[1], maxRadius=circle_radius_max[1])
            if hough_para2_inc < 0.0001:
                channel_ball_1 = cv2.GaussianBlur(channel_ball_1,(0, 0),1)
                gaussian_blur_para = gaussian_blur_para + 1
                end_signal_3 = 1
#                gaussian_blur_para = gaussian_blur_para + 1
                print("[IMG]:Gaussian blur parameter increased")
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
            if showplot == 1:
                print("Ball1: Current Hougg para2 = " + str(hough_para2))
    circles_info[0][1] = circles[0][0] 
                
    # Ball 2 channel-----------------------------------------------------------
    gaussian_blur_para = 1
    end_signal_hough = 0
    while end_signal_hough == 0:
        hough_para2 = 10
        hough_para2_inc = 5
        end_signal_3 = 0
        old_num_circles = 1000
        
        if gaussian_blur_para >=5:
            print("[ERROR]:Hough circle detect failed")
            return -1
    
        while end_signal_3 == 0:
            circles = cv2.HoughCircles(channel_ball_2,cv2.HOUGH_GRADIENT,1,10,
                                   param1=100, param2=hough_para2, minRadius=circle_radius_min[2], maxRadius=circle_radius_max[2])
            if hough_para2_inc < 0.0001:
                channel_ball_2 = cv2.GaussianBlur(channel_ball_2,(0, 0),1)
                gaussian_blur_para = gaussian_blur_para + 1
                end_signal_3 = 1
#                gaussian_blur_para = gaussian_blur_para + 1
                print("[IMG]:Gaussian blur parameter increased")
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
            if showplot == 1:
                print("Ball2: Current Hough para2 = " + str(hough_para2))
    circles_info[0][2] = circles[0][0] 
        
    for i in circles_info:
        counter=0
        for j in i: #extract center and radius of the three circles
            circle_temp[counter].center = (int(j[0]), int(j[1]))
            circle_temp[counter].radius = int(j[2])
           
            # draw center
            #cv2.circle(img, circle_temp[counter].center, 3, (0, 255, 0), -1, 8, 0)
            # 绘制圆轮廓
            cv2.circle(img_origin, circle_temp[counter].center, circle_temp[counter].radius, (255, 255, 255), 1, 1, 0)
                
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
                cv2.circle(img_origin, (pointX, pointY), 1, draw_color, 1, 1, 0)
                
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
        cv2.imwrite("out_put_img_before_color_assign.jpg",img_origin)   
        cv2.imshow("img",img_origin)
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

    cv2.circle(img_origin, (int(circle_centers[0][0]),int(circle_centers[0][1])), 1, (255, 50, 50), 1, 1, 0)
    cv2.circle(img_origin, (int(circle_centers[1][0]),int(circle_centers[1][1])), 1, (50, 255, 50), 1, 1, 0)
    cv2.circle(img_origin, (int(circle_centers[2][0]),int(circle_centers[2][1])), 1, (0, 0, 0), 1, 1, 0)
    
     
    if showplot == 1:        
        cv2.imwrite("out_put_img.jpg",img_origin)   
        cv2.imshow("show",img_origin)
        #cv2.imshow("show",gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
    return circle_centers, circle_radius, img_origin

def circle_center_detect (img, showplot, circle_radius_min, circle_radius_max, min_center_distance):
    
    # constant defination
    pi = math.pi
    color_detect3_threshhold = 20
    sample_number = 30
    
    circle_radius_min = int(circle_radius_min)
    circle_radius_max = int(circle_radius_max)

    gaussian_blur_para = 1
    
    circle_temp = [circle_temp_class(), circle_temp_class(), circle_temp_class()]
    
    h, w = img.shape[:2]

    red = np.asarray(img[:,:,2])
    green = np.asarray(img[:,:,1])
    blue = np.asarray(img[:,:,0])
    ones = np.ones((h,w))
    new = (ones-np.multiply((ones-red/255),(ones-green/255)))*255
    gray = np.uint8(new) 

    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
   
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
#                gaussian_blur_para = gaussian_blur_para + 1
                print("[IMG]:Gaussian blur parameter increased")
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


