# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

class color_threshold:
    ball0_ref_points = np.zeros((10,3))
    ball1_ref_points = np.zeros((10,3))
    ball2_ref_points = np.zeros((10,3))
    
    ball0_ref_points = np.array([[11,26,11],
                                [21,30,17],
                                [22,33,12],
                                [22,30,19],
                                [23,34,16],
                                [24,35,17],
                                [26,34,22],
                                [26,41,20],
                                [27,43,24],
                                [27,58,54],
                                [28,47,44],
                                [29,47,24],
                                [31,37,27],
                                [33,38,28],
                                [34,70,69],
                                [34,36,27],
                                [35,63,35],
                                [37,45,19],
                                [37,47,30],
                                [39,84,81],
                                [40,47,27],
                                [40,45,21],
                                [41,48,30],
                                [42,67,38],
                                [45,53,32],
                                [50,68,38],
                                [52,63,33],
                                [62,82,36],
                                [64,68,33],
                                [69,94,39],
                                [70,77,50],
                                [75,80,48],
                                [79,86,47],
                                [80,110,46],
                                [85,89,51],
                                [87,105,56],
                                [87,97,53],
                                [93,115,55],
                                [93,113,50],
                                [95,115,60],
                                [99,122,66],
                                [102,107,66],
                                [114,136,80],
                                [119,127,70],
                                [135,123,70],
                                [216,251,163],
                                [171,221,139],
                                [177,218,137],
                                [143,199,114],
                                [139,176,97],
                                [192,250,178],
                                [175,237,153],
                                [160,219,132],
                                [151,215,140],
                                [127,192,104]])
    

    ball1_ref_points = np.array([[10,50,56],
                                [13,54,62],
                                [18,38,37],
                                [19,40,46],
                                [22,50,48],
                                [23,67,74],
                                [24,59,55],
                                [24,51,58],
                                [27,58,54],
                                [28,64,62],
                                [28,47,44],
                                [32,62,64],
                                [34,70,69],
                                [35,69,67],
                                [38,65,64],
                                [39,84,81],
                                [41,80,78],
                                [45,67,64],
                                [50,58,57],
                                [52,115,128],
                                [52,97,94],
                                [54,77,73],
                                [56,133,127],
                                [63,109,114],
                                [67,108,110],
                                [71,128,119],
                                [78,107,109],
                                [91,185,189],
                                [92,166,189],
                                [93,156,160],
                                [95,136,130],
                                [96,206,194],
                                [115,136,139],
                                [117,195,230],
                                [120,232,216],
                                [123,226,250],
                                [126,222,223],
                                [145,229,252],
                                [145,210,218],
                                [145,160,160],
                                [151,237,233],
                                [163,234,224],
                                [167,221,230],
                                [185,195,192],
                                [201,229,224],
                                [148,154,156],
                                [139,174,168],
                                [164,180,178],
                                [173,191,191],
                                [177,195,192],
                                [147,169,169],
                                [186,188,184],
                                [152,178,180],
                                [152,185,187]])

    
    
    ball2_ref_points = np.array([[8,8,42],
                                [16,22,51],
                                [17,18,41],
                                [17,17,42],
                                [17,15,75],
                                [17,20,50],
                                [18,20,49],
                                [21,21,45],
                                [22,27,66],
                                [22,22,48],
                                [23,19,47],
                                [23,23,53],
                                [25,20,107],
                                [26,28,109],
                                [29,27,110],
                                [36,34,95],
                                [36,28,106],
                                [40,30,76],
                                [41,30,121],
                                [41,32,82],
                                [41,32,90],
                                [45,43,128],
                                [49,35,145],
                                [57,37,152],
                                [59,51,162],
                                [60,56,167],
                                [61,52,152],
                                [64,44,170],
                                [68,47,144],
                                [71,49,140],
                                [71,45,134],
                                [72,69,192],
                                [74,67,190],
                                [81,70,204],
                                [85,82,203],
                                [85,69,210],
                                [86,56,145],
                                [90,60,147],
                                [92,68,243],
                                [104,74,192],
                                [116,78,254],
                                [126,87,252],
                                [140,86,172],
                                [164,50,64],
                                [169,113,200]])


    
    ball0_blue_curve_coeff = None
    ball0_green_curve_coeff = None
    ball0_red_curve_coeff = None
    
    ball1_blue_curve_coeff = None
    ball1_green_curve_coeff = None
    ball1_red_curve_coeff = None
    
    ball2_blue_curve_coeff = None
    ball2_green_curve_coeff = None
    ball2_red_curve_coeff = None
    
    def __init__(self):
        
        return None
    
    def color_polyfit(self, order_ball0=2 , order_ball1=2, order_ball2 = 2):
        ball0_ref_bright = np.sum( self.ball0_ref_points , axis = 1)
        self.ball0_blue_curve_coeff = np.polyfit (ball0_ref_bright , self.ball0_ref_points[:,0], order_ball0)
        self.ball0_green_curve_coeff = np.polyfit (ball0_ref_bright , self.ball0_ref_points[:,1], order_ball0)
        self.ball0_red_curve_coeff = np.polyfit (ball0_ref_bright , self.ball0_ref_points[:,2], order_ball0)
        
        ball1_ref_bright = np.sum( self.ball1_ref_points , axis = 1)
        self.ball1_blue_curve_coeff = np.polyfit (ball1_ref_bright , self.ball1_ref_points[:,0], order_ball1)
        self.ball1_green_curve_coeff = np.polyfit (ball1_ref_bright , self.ball1_ref_points[:,1], order_ball1)
        self.ball1_red_curve_coeff = np.polyfit (ball1_ref_bright , self.ball1_ref_points[:,2], order_ball1)
        
        ball2_ref_bright = np.sum( self.ball2_ref_points , axis = 1)
        self.ball2_blue_curve_coeff = np.polyfit (ball2_ref_bright , self.ball2_ref_points[:,0], order_ball2)
        self.ball2_green_curve_coeff = np.polyfit (ball2_ref_bright , self.ball2_ref_points[:,1], order_ball2)
        self.ball2_red_curve_coeff = np.polyfit (ball2_ref_bright , self.ball2_ref_points[:,2], order_ball2)
        
        return None
        
    def color_reference(self, sample_point):
        bright = np.sum(sample_point)
        # Ball 0 ---------------------------------------------------------------
        ball0_blue = np.polyval(self.ball0_blue_curve_coeff, bright)
        ball0_green = np.polyval(self.ball0_green_curve_coeff, bright)
        ball0_red = np.polyval(self.ball0_red_curve_coeff, bright)
        # Ball 1 ---------------------------------------------------------------
        ball1_blue = np.polyval(self.ball1_blue_curve_coeff, bright)
        ball1_green = np.polyval(self.ball1_green_curve_coeff, bright)
        ball1_red = np.polyval(self.ball1_red_curve_coeff, bright)
        # Ball 2 ---------------------------------------------------------------
        ball2_blue = np.polyval(self.ball2_blue_curve_coeff, bright)
        ball2_green = np.polyval(self.ball2_green_curve_coeff, bright)
        ball2_red = np.polyval(self.ball2_red_curve_coeff, bright)
        
        color_ref = np.array([[ball0_blue , ball0_green , ball0_red],
                              [ball1_blue , ball1_green , ball1_red],
                              [ball2_blue , ball2_green , ball2_red]])
        return color_ref
        
        
    def color_polyplot(self):
        bright = np.linspace(0,765,2000)
        # Ball 0 ---------------------------------------------------------------
        ball0_blue = np.polyval(self.ball0_blue_curve_coeff, bright)
        ball0_green = np.polyval(self.ball0_green_curve_coeff, bright)
        ball0_red = np.polyval(self.ball0_red_curve_coeff, bright)
        
        plt.figure(1)
        plt.plot(bright , ball0_blue, 'b' ,label = 'blue')
        plt.plot(bright , ball0_green, 'g' ,label = 'green')
        plt.plot(bright , ball0_red, 'r' ,label = 'red')
        plt.xlabel('bright')
        plt.ylabel('color value')
        plt.title('ball 0')
        
        for point in self.ball0_ref_points:
            plt.scatter(np.sum(point) , point[0] ,s=None, c='b')
            plt.scatter(np.sum(point) , point[1] ,s=None, c='g')
            plt.scatter(np.sum(point) , point[2] ,s=None, c='r')
        
        # Ball 1 ---------------------------------------------------------------
        ball1_blue = np.polyval(self.ball1_blue_curve_coeff, bright)
        ball1_green = np.polyval(self.ball1_green_curve_coeff, bright)
        ball1_red = np.polyval(self.ball1_red_curve_coeff, bright)
        
        plt.figure(2)
        plt.plot(bright , ball1_blue, 'b' ,label = 'blue')
        plt.plot(bright , ball1_green, 'g' ,label = 'green')
        plt.plot(bright , ball1_red, 'r' ,label = 'red')
        plt.xlabel('bright')
        plt.ylabel('color value')
        plt.title('ball 1')
        
        for point in self.ball1_ref_points:
            plt.scatter(np.sum(point) , point[0] ,s=None, c='b')
            plt.scatter(np.sum(point) , point[1] ,s=None, c='g')
            plt.scatter(np.sum(point) , point[2] ,s=None, c='r')
        
        # Ball 2 ---------------------------------------------------------------
        ball2_blue = np.polyval(self.ball2_blue_curve_coeff, bright)
        ball2_green = np.polyval(self.ball2_green_curve_coeff, bright)
        ball2_red = np.polyval(self.ball2_red_curve_coeff, bright)
        
        plt.figure(3)
        plt.plot(bright , ball2_blue, 'b' ,label = 'blue')
        plt.plot(bright , ball2_green, 'g' ,label = 'green')
        plt.plot(bright , ball2_red, 'r' ,label = 'red')
        plt.xlabel('bright')
        plt.ylabel('color value')
        plt.title('ball 2')
        
        for point in self.ball2_ref_points:
            plt.scatter(np.sum(point) , point[0] ,s=None, c='b')
            plt.scatter(np.sum(point) , point[1] ,s=None, c='g')
            plt.scatter(np.sum(point) , point[2] ,s=None, c='r')
            
        
        