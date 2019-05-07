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
import func_color_threshold as fcth
from multiprocessing.pool import ThreadPool

color_threshold = fcth.color_threshold()
color_threshold.color_polyfit()
saturation_enhance = 1

class circle_temp_class:
    center = None
    radius = None
    color_vec = np.array([0,0,0])

# return class of the function: circle_center_detect, contains the center of the three color circles [B, G, R]
class circle_class:
    b = np.array([0,0])
    g = np.array([0,0])
    r = np.array([0,0])

def circle_center_detect_single_ball (img, showplot, circles_radius_min, circles_radius_max, ref_color, num_ball, idx_cam, carve_sign, carve_center, carve_radius):
    img_origin = img
    pi = math.pi
    color_detect3_threshhold = 20
    sample_number = 36
    circle_trust_threshold = 0.15
    
    
    circle_temp = [circle_temp_class(), circle_temp_class(), circle_temp_class()]

    h, w = img.shape[:2]
    red = np.float32(img[:,:,2])
    green = np.float32(img[:,:,1])
    blue = np.float32(img[:,:,0])   

    red_new = (np.square(red/50)*900).clip(min=0,max=255)
    green_new = (np.square(green/50)*900).clip(min=0,max=255)
    blue_new = (np.square(blue/50)*900).clip(min=0,max=255) 

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

    canny_edge = cv2.Canny(cv2.GaussianBlur(gray_gauss_sum, (0,0), 1),40,70)
    combine = np.zeros((h,w,3))
    for i in range(3):
        combine[:,:,i] += (np.float32(canny_edge)+np.float32(img[:,:,i])).clip(min=0,max=255)
        
    if showplot == 1:
        cv2.imshow("canny",canny_edge) 
        cv2.imshow("canny on origin",np.uint8(combine))
        cv2.waitKey(0)
        cv2.destroyAllWindows() 

    channel_ball_2 = np.uint8((3*(red-green)).clip(min=0,max=255)) # red
    channel_ball_0 = np.uint8((3*(green-red)).clip(min=0,max=255)) # green
    channel_ball_1 = np.uint8((10*(red-blue)-7*np.float32(channel_ball_2)).clip(min=0,max=255)) # yellow
    channel_ball_0 = np.uint8((3*(np.float32(channel_ball_0)-2*np.float32(channel_ball_1))).clip(min=0,max=255)) # green
    channel_ball_2 = np.uint8((3*(np.float32(channel_ball_2)-3*np.float32(channel_ball_1))).clip(min=0,max=255)) # red
    
    if showplot == 1:
        cv2.imshow("green channel",channel_ball_0)
        cv2.imshow("yellow channel ",channel_ball_1)
        cv2.imshow("red channel",channel_ball_2)

    blur_param = 7
    binary_thresh = 30
    (T,channel_ball_0) = cv2.threshold(cv2.GaussianBlur(channel_ball_0, (0,0), blur_param),binary_thresh,255,cv2.THRESH_BINARY)
    (T,channel_ball_1) = cv2.threshold(cv2.GaussianBlur(channel_ball_1, (0,0), blur_param),binary_thresh,255,cv2.THRESH_BINARY)
    (T,channel_ball_2) = cv2.threshold(cv2.GaussianBlur(channel_ball_2, (0,0), blur_param),binary_thresh,255,cv2.THRESH_BINARY)

    channel_ball_0 = np.uint8(np.multiply(np.float32(channel_ball_0)/255,canny_edge))
    channel_ball_1 = np.uint8(np.multiply(np.float32(channel_ball_1)/255,canny_edge))
    channel_ball_2 = np.uint8(np.multiply(np.float32(channel_ball_2)/255,canny_edge))

#    channel_ball_0 = cv2.GaussianBlur(channel_ball_0, (0,0), 1)
#    channel_ball_1 = cv2.GaussianBlur(channel_ball_1, (0,0), 1)
#    channel_ball_2 = cv2.GaussianBlur(channel_ball_2, (0,0), 1)
#    
#    channel_ball_0 = cv2.GaussianBlur(channel_ball_0, (0,0), 1)
#    channel_ball_1 = cv2.GaussianBlur(channel_ball_1, (0,0), 1)
#    channel_ball_2 = cv2.GaussianBlur(channel_ball_2, (0,0), 1)
#    
#    channel_ball_0 = np.uint8(((np.float32(channel_ball_0)-25*np.ones((h,w)))*255).clip(min=0,max=255))
#    channel_ball_1 = np.uint8(((np.float32(channel_ball_1)-25*np.ones((h,w)))*255).clip(min=0,max=255))
#    channel_ball_2 = np.uint8(((np.float32(channel_ball_2)-25*np.ones((h,w)))*255).clip(min=0,max=255))
    
    if showplot == 1:
        cv2.imshow("green",channel_ball_0)
        cv2.imshow("yellow",channel_ball_1)
        cv2.imshow("red",channel_ball_2)
        
        # cv2.imwrite("0green_blured_canny.jpg",channel_ball_0)
        # cv2.imwrite("0yellow_blured_canny.jpg",channel_ball_1)
        # cv2.imwrite("0red_blured_canny.jpg",channel_ball_2)
        #cv2.imshow("show",gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
    
    # denoise for color image and enhance the saturation
    img = cv2.GaussianBlur(img, (0,0), 3)
    if saturation_enhance == 1:          
        saturation_factor = 3
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_new = np.uint8(cv2.pow(hsv/255,1/saturation_factor)*255)
        hsv[:,:,1] = hsv_new[:,:,1]
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    circles_info = np.zeros([1,3,3]) # Initialize circles
    circle_numbers = 1
    hough_para = 10 
    hough_para_inc = 5
    hough_para_threshold = 0.01

    # circle_0 = auto_hough_circle(channel_ball_0 , circle_numbers, showplot , np.int_(circles_radius_min[0]), np.int_(circles_radius_max[0]), hough_para, hough_para_inc, hough_para_threshold)
    # circle_1 = auto_hough_circle(channel_ball_1 , circle_numbers, showplot , np.int_(circles_radius_min[1]), np.int_(circles_radius_max[1]), hough_para, hough_para_inc, hough_para_threshold)
    # circle_2 = auto_hough_circle(channel_ball_2 , circle_numbers, showplot , np.int_(circles_radius_min[2]), np.int_(circles_radius_max[2]), hough_para, hough_para_inc, hough_para_threshold)

    # multi-thread process version
    pool = ThreadPool(processes=3)
    async_result_0 = pool.apply_async(auto_hough_circle, (channel_ball_0 , circle_numbers, showplot , np.int_(circles_radius_min[0]), np.int_(circles_radius_max[0]), hough_para, hough_para_inc, hough_para_threshold)) # tuple of args for foo
    async_result_1 = pool.apply_async(auto_hough_circle, (channel_ball_1 , circle_numbers, showplot , np.int_(circles_radius_min[1]), np.int_(circles_radius_max[1]), hough_para, hough_para_inc, hough_para_threshold)) # tuple of args for foo
    async_result_2 = pool.apply_async(auto_hough_circle, (channel_ball_2 , circle_numbers, showplot , np.int_(circles_radius_min[2]), np.int_(circles_radius_max[2]), hough_para, hough_para_inc, hough_para_threshold)) # tuple of args for foo
    circle_0 = async_result_0.get()
    circle_1 = async_result_1.get()
    circle_2 = async_result_2.get()


    ############### carve out image circle #############################
    if carve_sign == 1:
        mask_0 = cv2.circle(np.zeros((h,w)),(carve_center[0][0],carve_center[0][1]), int(carve_radius[0]+5), 255, -1)
        mask_0 = cv2.circle(mask_0,(carve_center[0][0],carve_center[0][1]), int(carve_radius[0]-3), 0, -1)

        mask_1 = cv2.circle(np.zeros((h,w)),(carve_center[1][0],carve_center[1][1]), int(carve_radius[1]+5), 255, -1)
        mask_1 = cv2.circle(mask_1,(carve_center[1][0],carve_center[1][1]), int(carve_radius[1]-3), 0, -1)

        mask_2 = cv2.circle(np.zeros((h,w)),(carve_center[2][0],carve_center[2][1]), int(carve_radius[2]+5), 255, -1)
        mask_2 = cv2.circle(mask_2,(carve_center[2][0],carve_center[2][1]), int(carve_radius[2]-3), 0, -1)

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

    circle_centers = np.zeros((3,2))
    circle_radius = np.zeros(3)

    for i in circles_info:
        counter=0
        for j in i: #extract center and radius of the three circles
            circle_temp[counter].center = (int(j[0]), int(j[1]))
            circle_temp[counter].radius = int(j[2])
           
            # draw center
            #cv2.circle(img, circle_temp[counter].center, 3, (0, 255, 0), -1, 8, 0)
            # 绘制圆轮廓
            cv2.circle(img_origin, circle_temp[counter].center, circle_temp[counter].radius, (255, 255, 255), 1, 1, 0)

            # different color point number list: (num_color_ball0, num_color_ball1, num_color_ball2)     
            sample_color_count = np.zeros(3)

            #sample points to detect color
            for k in range(0, sample_number):
                pointX = int(round(circle_temp[counter].center[0] + 0.7*circle_temp[counter].radius * np.sin (2*k*pi/sample_number)))
                pointY = int(round(circle_temp[counter].center[1] + 0.7*circle_temp[counter].radius * np.cos (2*k*pi/sample_number)))
                
                try:
                    pointColor = img[pointY, pointX]  # [IMPORTANT] Notice that in the index, x and y are reversed
                except:
                    pointColor = np.array([0,0,0])
                #detected_color = color_detect(pointColor, blue_ref, green_ref, red_ref, ref_threshhold)
                detected_color = color_detect(pointColor, color_detect3_threshhold)
                try:
                    draw_color = img[pointY, pointX]
                except:
                    draw_color = np.array([0,0,0])
                    
                if np.sum(detected_color) > 1:
                    draw_color = np.array((255,255,255))
                elif np.sum(detected_color) == 0:
                    draw_color = np.array((0,0,0))
                draw_color = (float(draw_color[0]),float(draw_color[1]),float(draw_color[2]))
                
                circle_temp[counter].color_vec = circle_temp[counter].color_vec + detected_color
                if detected_color[0] == 1:               
                    cv2.circle(img_origin, (pointX, pointY), 1, [0,255,0], 1, 1, 0)
                    sample_color_count[0] = 1 + sample_color_count[0] 
                elif detected_color[1] == 1:
                    cv2.circle(img_origin, (pointX, pointY), 1, [0,255,255], 1, 1, 0)
                    sample_color_count[1] = 1 + sample_color_count[1] 
                elif detected_color[2] == 1:
                    cv2.circle(img_origin, (pointX, pointY), 1, [0,0,255], 1, 1, 0)
                    sample_color_count[2] = 1 + sample_color_count[2]
                else:
                    cv2.circle(img_origin, (pointX, pointY), 1, [0,0,0], 1, 1, 0)
                                
            if sample_color_count[counter] > circle_trust_threshold*sample_number:
                circle_centers[counter % 3] = circle_temp[counter % 3].center
                circle_radius[counter %3] = circle_temp[counter % 3].radius
            counter = counter + 1
    
#     circle_color_counter = np.zeros((3,3))

        
    if showplot == 1:
        cv2.imwrite("out_put_img_before_color_assign.jpg",img_origin)   
        cv2.imshow("img",img_origin)
        #cv2.imshow("show",gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 

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
        print("circle_radius\n",circle_radius)
        
    # #[test]: currently the circle is not seperated successfully, so if one circle is failed, the whole image is failed
    # if (circle_radius[0]*circle_radius[1]*circle_radius[2]) == 0:
    #     circle_centers = np.zeros((3,2))
    #     circle_radius = np.zeros(3)
    # #[test]
    
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
            return np.zeros((1,1,3))
    
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
            # if show_info == 1:
            #     print("Current Hough para2 = " + str(hough_para2))
                
    # if circles.any() == None:
    #     circles = np.zeros((1,1,3))
                
    return circles    
    

def color_detect (target_color, threshhold):
    
    # return color
    color = np.array((0,0,0))
    color_ref = color_threshold.color_reference(target_color)
    brightness = np.sum(target_color)
    
#    if brightness<45 or brightness>700:
    if ((np.std(target_color)*3-3)/(brightness + 30)) < 0.25:
        return color

    diff_ball_0 = np.square(target_color[0]-color_ref[0,0])+np.square(target_color[1]-color_ref[0,1])+np.square(target_color[2]-color_ref[0,2])
    diff_ball_1 = np.square(target_color[0]-color_ref[1,0])+np.square(target_color[1]-color_ref[1,1])+np.square(target_color[2]-color_ref[1,2])
    diff_ball_2 = np.square(target_color[0]-color_ref[2,0])+np.square(target_color[1]-color_ref[2,1])+np.square(target_color[2]-color_ref[2,2])
    diff_background = np.square(target_color[0]-brightness/3)+np.square(target_color[1]-brightness/3)+np.square(target_color[2]-brightness/3)

    # diff_ball_0 = np.square(target_color[0]-color_ref[0,0])+np.square(target_color[1]-color_ref[0,1])+np.square(target_color[2]-color_ref[0,2])
    # diff_ball_1 = np.square(target_color[0]-color_ref[1,0])+np.square(target_color[1]-color_ref[1,1])+np.square(target_color[2]-color_ref[1,2])
    # diff_ball_2 = np.square(target_color[0]-color_ref[2,0])+np.square(target_color[1]-color_ref[2,1])+np.square(target_color[2]-color_ref[2,2])
    # diff_background = np.square(target_color[0]-brightness)+np.square(target_color[1]-brightness)+np.square(target_color[2]-brightness)

    diff_list = np.array([diff_ball_0,diff_ball_1,diff_ball_2,diff_background+0])
    min_index = diff_list.argmin()
    if min_index == 0:
        color[0] = 1
    if min_index == 1:
        color[1] = 1
    if min_index == 2:
        color[2] = 1
    return color



# boolize function, takes array as input, and output a same sized array with only 0 or 1    
def boolize (arr_origin):
    arr = arr_origin
    for i in range(0, len(arr)):
        if arr[i] <= 0:
            arr[i] = 0
        else:
            arr[i] = 1
    return arr


