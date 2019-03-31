# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

class color_threshold:
    ball0_ref_points = np.zeros((10,3))
    ball1_ref_points = np.zeros((10,3))
    ball2_ref_points = np.zeros((10,3))
    
    ball0_ref_points[0] = [104,80,47]
    ball0_ref_points[1] = [119,99,75]
    ball0_ref_points[2] = [77,114,123]
    ball0_ref_points[3] = [121,111,99]
    ball0_ref_points[4] = [126,114,96]
    ball0_ref_points[5] = [142,134,104]
    ball0_ref_points[6] = [161,147,119]
    ball0_ref_points[7] = [116,134,158]
    ball0_ref_points[8] = [118,111,103]
    ball0_ref_points[9] = [107,101,90]
    
    ball1_ref_points[0] = [107,160,88]
    ball1_ref_points[1] = [64,140,70]
    ball1_ref_points[2] = [76,135,55]
    ball1_ref_points[3] = [157,204,151]
    ball1_ref_points[4] = [76,146,91]
    ball1_ref_points[5] = [139,176,109]
    ball1_ref_points[6] = [147,191,131]
    ball1_ref_points[7] = [158,208,147]
    ball1_ref_points[8] = [85,148,94]
    ball1_ref_points[9] = [123,178,126]
    
    ball2_ref_points[0] = [105,132,161]
    ball2_ref_points[1] = [104,138,172]
    ball2_ref_points[2] = [105,112,184]
    ball2_ref_points[3] = [44,69,148]
    ball2_ref_points[4] = [15,32,102]
    ball2_ref_points[5] = [25,29,105]
    ball2_ref_points[6] = [21,23,115]
    ball2_ref_points[7] = [31,38,110]
    ball2_ref_points[8] = [36,45,111]
    ball2_ref_points[9] = [98,115,175]
    
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
        
#    def color_reference(self, )
        
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
            
        
        