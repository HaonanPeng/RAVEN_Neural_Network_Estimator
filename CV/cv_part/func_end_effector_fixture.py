# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 17:22:55 2019

@author: Xingjian Yang
"""

import cv2
import math
import numpy as np



def end_effector_fixture(ball_center,d_ball2center):
    ball_1 = ball_center[0]
    ball_2 = ball_center[1]
    ball_3 = ball_center[2]
    
    #surface: a*x + b*y + c*z + d = 0
    a = (ball_2[1]-ball_1[1])*(ball_3[2]-ball_1[2])-(ball_3[1]-ball_1[1])*(ball_2[2]-ball_1[2])
    b = (ball_2[2]-ball_1[2])*(ball_3[0]-ball_1[0])-(ball_3[2]-ball_1[2])*(ball_2[0]-ball_1[0])
    c = (ball_2[0]-ball_1[0])*(ball_3[1]-ball_1[1])-(ball_3[0]-ball_1[0])*(ball_2[1]-ball_1[1])
    d = -a*ball_1[0]-b*ball_1[1]-c*ball_1[2]
#    print('a,b,c,d\n',a,b,c,d，,'\n\n')
    
    normal = [a,b,c]/np.sqrt(a**2+b**2+c**2)
    y_axis = (ball_3-ball_1)/np.linalg.norm(ball_3-ball_1)
    x_axis = np.cross(y_axis,normal)
#    print('x_axis\n',x_axis,'\n\n')
#    print('y_axis\n',y_axis,'\n\n')
    
    # set ball_1 as the origin of the plane, planarize 3 balls' coordinate
    ball_1p = np.array([0,0])
    ball_2p = np.array([np.dot(x_axis,ball_2-ball_1),np.dot(y_axis,ball_2-ball_1)])
    ball_3p = np.array([0,np.linalg.norm(ball_1-ball_3)])
    center_p = np.array([(ball_1p[0]+ball_3p[0]+ball_2p[0]-d_ball2center)/3,(ball_1p[1]+ball_2p[1]+ball_3p[1])/3])
    
#    print('ball_1p\n',ball_1p,'\n\n')
#    print('ball_2p\n',ball_2p,'\n\n')
#    print('ball_3p\n',ball_3p,'\n\n')
#    print('center_p\n',center_p,'\n\n')
    
    theta = np.arctan((-ball_1p[0]+ball_3p[0]+center_p[1]-ball_2p[1])/(ball_1p[1]-ball_3p[1]+center_p[0]-ball_2p[0]))
    print(theta)
    
    ball_2p_new = np.array([center_p[0]+np.cos(theta)*d_ball2center, center_p[1]+np.sin(theta)*d_ball2center])
    ball_3p_new = np.array([center_p[0]-np.sin(theta)*d_ball2center, center_p[1]+np.cos(theta)*d_ball2center])

    ball_2_new = ball_1+np.dot(ball_2p_new[0],x_axis)+np.dot(ball_2p_new[1],y_axis)
    ball_3_new = ball_1+np.dot(ball_3p_new[0],x_axis)+np.dot(ball_3p_new[1],y_axis)
    center =  ball_1+np.dot(center_p[0],x_axis)+np.dot(center_p[1],y_axis)
    
    x_axis_new = (ball_2_new-center)/np.linalg.norm(ball_2_new-center)
    y_axis_new = (ball_3_new-center)/np.linalg.norm(ball_3_new-center)
    z_axis_new = np.cross(x_axis_new,y_axis_new)
    
#    print(ball_3_new)
#    print(ball_2p_new)
#    print(ball_3_new)
#    print(ball_3p_new)
    
    print(x_axis_new)
    print(y_axis_new)
    
    return center 
    
#ball_center = np.array([[1,0,0],[0,1,0],[0,0,1]])+np.random.rand(3,3)*0.2
ball_center = np.array([[1,0,0],[0,1,0],[0,0,1]])
ball_center = np.array([[0,-1,0],[1,0,0],[0,1,0]])+np.random.rand(3,3)*0.1
end_effector_fixture(ball_center,1)




