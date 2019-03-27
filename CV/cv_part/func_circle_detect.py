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

def circle_center_detect_single_ball (img, showplot, circles_radius_min, circles_radius_max, ref_color, num_ball, idx_cam):
    img_origin = img
    pi = math.pi
    color_detect3_threshhold = 20
    sample_number = 30
    sign_carve = 1
    
    circle_temp = [circle_temp_class(), circle_temp_class(), circle_temp_class()]

    h, w = img.shape[:2]
    red = np.float32(img[:,:,2])
    green = np.float32(img[:,:,1])
    blue = np.float32(img[:,:,0])   

    red_new = (np.square(red/80)*800).clip(min=0,max=255)
    green_new = (np.square(red/80)*800).clip(min=0,max=255)
    blue_new = (np.square(red/80)*800).clip(min=0,max=255) 

    new_img = np.zeros((h,w,3))
    new_img[:,:,0] = blue_new
    new_img[:,:,1] = green_new
    new_img[:,:,2] = red_new
    gray = cv2.cvtColor(np.uint8(new_img),cv2.COLOR_BGR2GRAY)
    gray_gauss_sum = np.zeros((h,w))
    for i in range(6):
        gray_gauss_sum += np.float32(cv2.GaussianBlur(gray, (0,0), i+1))
    gray_gauss_sum = np.uint8(gray_gauss_sum/(i+1))
    
    if showplot == 1:
        cv2.imshow("gray_gauss_sum",gray_gauss_sum)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 

    canny_edge = cv2.Canny(cv2.GaussianBlur(gray_gauss_sum, (0,0), 2),50,50)
    combine = np.zeros((h,w,3))
    for i in range(3):
        combine[:,:,i] += (np.float32(canny_edge)+np.float32(img[:,:,i])).clip(min=0,max=255)
        
    if showplot == 1:
        cv2.imshow("canny",canny_edge) 
        cv2.imshow("canny on origin",np.uint8(combine))
        cv2.waitKey(0)
        cv2.destroyAllWindows() 

    if (idx_cam == 0) or (idx_cam == 1):
        channel_ball_2 = np.uint8((3*(red-green)).clip(min=0,max=255)) # red
        channel_ball_0 = np.uint8((3*(green-red)).clip(min=0,max=255)) # green
        channel_ball_1 = np.uint8((2*((red-blue)).clip(min=0,max=255)-channel_ball_2).clip(min=0,max=255))  # yellow
        channel_ball_2 = np.uint8((3*(np.float32(channel_ball_2)-np.float32(channel_ball_1))).clip(min=0,max=255)) # red
    elif (idx_cam == 2) or (idx_cam == 3):
        channel_ball_2 = np.uint8((3*(red-green)).clip(min=0,max=255)) # red
        channel_ball_0 = np.uint8((3*(green-red)).clip(min=0,max=255)) # green
        channel_ball_1 = np.uint8((3*((red-blue)).clip(min=0,max=255)-channel_ball_2).clip(min=0,max=255))  # yellow
        channel_ball_0 = np.uint8((3*(np.float32(channel_ball_0)-2*np.float32(channel_ball_1))).clip(min=0,max=255)) # green
    
    blur_param = 7
    binary_thresh = 30
    (T,channel_ball_0) = cv2.threshold(cv2.GaussianBlur(channel_ball_0, (0,0), blur_param),binary_thresh,255,cv2.THRESH_BINARY)
    (T,channel_ball_1) = cv2.threshold(cv2.GaussianBlur(channel_ball_1, (0,0), blur_param),binary_thresh,255,cv2.THRESH_BINARY)
    (T,channel_ball_2) = cv2.threshold(cv2.GaussianBlur(channel_ball_2, (0,0), blur_param),binary_thresh,255,cv2.THRESH_BINARY)

    channel_ball_0 = np.uint8(np.multiply(np.float32(channel_ball_0)/255,canny_edge))
    channel_ball_1 = np.uint8(np.multiply(np.float32(channel_ball_1)/255,canny_edge))
    channel_ball_2 = np.uint8(np.multiply(np.float32(channel_ball_2)/255,canny_edge))

    channel_ball_0 = cv2.GaussianBlur(channel_ball_0, (0,0), 1)
    channel_ball_1 = cv2.GaussianBlur(channel_ball_1, (0,0), 1)
    channel_ball_2 = cv2.GaussianBlur(channel_ball_2, (0,0), 1)
    
    channel_ball_0 = np.uint8(((np.float32(channel_ball_0)-75*np.ones((h,w)))*255).clip(min=0,max=255))
    channel_ball_1 = np.uint8(((np.float32(channel_ball_1)-75*np.ones((h,w)))*255).clip(min=0,max=255))
    channel_ball_2 = np.uint8(((np.float32(channel_ball_2)-75*np.ones((h,w)))*255).clip(min=0,max=255))
    
    if showplot == 1:
        cv2.imshow("green",channel_ball_0)
        cv2.imshow("yellow",channel_ball_1)
        cv2.imshow("red",channel_ball_2)
        
        cv2.imwrite("0green_blured_canny.jpg",channel_ball_0)
        cv2.imwrite("0yellow_blured_canny.jpg",channel_ball_1)
        cv2.imwrite("0red_blured_canny.jpg",channel_ball_2)
        #cv2.imshow("show",gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
    
    # denoise for color image
    img = cv2.GaussianBlur(img, (0,0), 4)
    
    circles_info = np.zeros([1,3,3]) # Initialize circles
    circle_numbers = 1
    hough_para = 10 
    hough_para_inc = 5
    hough_para_threshold = 0.01
    circle_0 = auto_hough_circle(channel_ball_0 , circle_numbers, showplot , np.int_(circles_radius_min[0]), np.int_(circles_radius_max[0]), hough_para, hough_para_inc, hough_para_threshold)
    circle_1 = auto_hough_circle(channel_ball_1 , circle_numbers, showplot , np.int_(circles_radius_min[1]), np.int_(circles_radius_max[1]), hough_para, hough_para_inc, hough_para_threshold)
    circle_2 = auto_hough_circle(channel_ball_2 , circle_numbers, showplot , np.int_(circles_radius_min[2]), np.int_(circles_radius_max[2]), hough_para, hough_para_inc, hough_para_threshold)

    ############### carve out image circle #############################
    if sign_carve == 1:
        mask_0 = cv2.circle(np.zeros((h,w)),(circle_0[0][0][0],circle_0[0][0][1]), int(circle_0[0][0][2]+5), 255, -1)
        mask_0 = cv2.circle(mask_0,(circle_0[0][0][0],circle_0[0][0][1]), int(circle_0[0][0][2]-3), 0, -1)

        mask_1 = cv2.circle(np.zeros((h,w)),(circle_1[0][0][0],circle_1[0][0][1]), int(circle_1[0][0][2]+5), 255, -1)
        mask_1 = cv2.circle(mask_1,(circle_1[0][0][0],circle_1[0][0][1]), int(circle_1[0][0][2]-3), 0, -1)

        mask_2 = cv2.circle(np.zeros((h,w)),(circle_2[0][0][0],circle_2[0][0][1]), int(circle_2[0][0][2]+5), 255, -1)
        mask_2 = cv2.circle(mask_2,(circle_2[0][0][0],circle_2[0][0][1]), int(circle_2[0][0][2]-3), 0, -1)

        channel_ball_0 = np.uint8(np.multiply(mask_0/255,channel_ball_0))
        channel_ball_1 = np.uint8(np.multiply(mask_1/255,channel_ball_1))
        channel_ball_2 = np.uint8(np.multiply(mask_2/255,channel_ball_2))

        circle_0 = auto_hough_circle(channel_ball_0 , circle_numbers, showplot , np.int_(circles_radius_min[0]), np.int_(circles_radius_max[0]), hough_para, hough_para_inc, hough_para_threshold)
        circle_1 = auto_hough_circle(channel_ball_1 , circle_numbers, showplot , np.int_(circles_radius_min[1]), np.int_(circles_radius_max[1]), hough_para, hough_para_inc, hough_para_threshold)
        circle_2 = auto_hough_circle(channel_ball_2 , circle_numbers, showplot , np.int_(circles_radius_min[2]), np.int_(circles_radius_max[2]), hough_para, hough_para_inc, hough_para_threshold)
        
        if showplot == 1:
            # cv2.imshow("mask_0",mask_0)
            # cv2.imshow("mask_1",mask_1)
            # cv2.imshow("mask_2",mask_2)
            cv2.imshow("green_carve",channel_ball_0)
            cv2.imshow("yellow_carve",channel_ball_1)
            cv2.imshow("red_carve",channel_ball_2)
            cv2.waitKey(0)
            cv2.destroyAllWindows() 
    
    ####################################################################

    circles_info[0][0] = circle_0[0][0] 
    circles_info[0][1] = circle_1[0][0] 
    circles_info[0][2] = circle_2[0][0] 


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
                detected_color = color_detect(pointColor, color_detect3_threshhold)
                
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

    canny_edge_new = cv2.cvtColor(canny_edge,cv2.COLOR_GRAY2RGB)
    cv2.circle(canny_edge_new, (int(circle_centers[0][0]),int(circle_centers[0][1])), 1, (255, 50, 50), 1, 1, 0)
    cv2.circle(canny_edge_new, (int(circle_centers[1][0]),int(circle_centers[1][1])), 1, (50, 255, 50), 1, 1, 0)
    cv2.circle(canny_edge_new, (int(circle_centers[2][0]),int(circle_centers[2][1])), 1, (0, 0, 0), 1, 1, 0)

    cv2.circle(canny_edge_new, (int(circle_centers[0][0]),int(circle_centers[0][1])), int(circle_radius[0]) ,(0, 255, 0), 1, 1, 0)
    cv2.circle(canny_edge_new, (int(circle_centers[1][0]),int(circle_centers[1][1])), int(circle_radius[1]) ,(0, 255, 255), 1, 1, 0)
    cv2.circle(canny_edge_new, (int(circle_centers[2][0]),int(circle_centers[2][1])), int(circle_radius[2]) ,(0, 0, 255), 1, 1, 0)
    
    if showplot == 1:        
        cv2.imwrite("out_put_img.jpg",img_origin)  
        cv2.imshow("canny+origin",canny_edge_new)
        cv2.imshow("show",img_origin)
        #cv2.imshow("show",gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
    return circle_centers, circle_radius, img_origin


def auto_hough_circle(img, circle_numbers =1 , show_info=0 , circle_radius_min=0, circle_radius_max=0 , hough_para=10, hough_para_inc=5, hough_para_threshold = 0.01):
    gaussian_blur_para = 1
    end_signal_hough = 0
    while end_signal_hough == 0:
        
        hough_para2 = 10
        hough_para2_inc = 5
        end_signal_3 = 0
        old_num_circles = 1000
        
        if gaussian_blur_para >=5:
            print("[ERROR]:Hough circle detect failed")
            return np.zeros((circle_numbers,2)), np.zeros(circle_numbers)
    
        while end_signal_3 == 0:
            circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,40,
                                   param1=100, param2=hough_para2, minRadius=circle_radius_min, maxRadius=circle_radius_max)
            if hough_para2_inc < (0.1*hough_para_threshold):
                img = cv2.GaussianBlur(img,(0, 0),1)
                gaussian_blur_para = gaussian_blur_para + 1
                end_signal_3 = 1
                print("[IMG]:Gaussian blur parameter increased")
            try:
                if len(circles[0]) > circle_numbers:
                    hough_para2 = hough_para2 + hough_para2_inc
                    if old_num_circles <=1:
                        hough_para2_inc = hough_para2_inc/2    
                if len(circles[0]) <= circle_numbers:
                    hough_para2 = hough_para2 - hough_para2_inc
                    if old_num_circles >=circle_numbers:
                        hough_para2_inc = hough_para2_inc/2
                if (len(circles[0]) == circle_numbers) & (old_num_circles > circle_numbers) & (hough_para2_inc < hough_para_threshold):
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
            if show_info == 1:
                print("Current Hough para2 = " + str(hough_para2))
                
    return circles    
    

def color_detect (target_color, threshhold):
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


