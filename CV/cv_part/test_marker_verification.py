import cv2
import math
import numpy as np
import func_circle_detect as f_cd
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


info_txt_path = 'Camera_Info_txt/'

info_P_chess = np.loadtxt(info_txt_path + 'info_P_chess.txt')
info_R_chess = np.loadtxt(info_txt_path + 'info_R_chess.txt')
info_P_cam2chess = np.loadtxt(info_txt_path + 'info_P_cam2chess.txt')
info_R_cam2chess = np.loadtxt(info_txt_path + 'info_R_cam2chess.txt')
info_P_cam = np.loadtxt(info_txt_path + 'info_P_cam.txt')
info_R_cam = np.loadtxt(info_txt_path + 'info_R_cam.txt')
info_cam0_marker = np.loadtxt(info_txt_path + 'info_cam0_marker.txt')
info_cam1_marker = np.loadtxt(info_txt_path + 'info_cam1_marker.txt')
info_cam2_marker = np.loadtxt(info_txt_path + 'info_cam2_marker.txt')
info_cam3_marker = np.loadtxt(info_txt_path + 'info_cam3_marker.txt')


class camera_info_definition():
    resolution = np.array([[1280,720]])  #photo resolution
    f = 4 # focal length of the camera (mm)
    ps = f/1420 # Pixel size in real world 
    
    P_chess = np.array([[0,0,0]]) #Chessboard origin P_cam2chess in System Coordinate
    R_chess = np.array([[1,0,0],[0,1,0],[0,0,1]]) #Chessboard Rotation Matrix in System coordinate
    
    P_cam2chess = np.array([[0,0,0]]) # camera P_cam2chess in Chessboard Coordinate (from Matlab camera_localization_Chessboard.m)
    R_cam2chess = np.array([[1,0,0],[0,1,0],[0,0,1]]) # camera rotation (from Matlab camera_localization_Chessboard.m)
    
    P_cam = np.array([[0,0,0]]) #camera P_cam in System coordinate
    R_cam = np.array([[1,0,0],[0,1,0],[0,0,1]]) #camera Rotation Matrix in System coordinate
    
    image_marker_coord = None  #Image coordinate of balls center; Image plane Origin: Leftup cornor
    image_marker_coord_lastframe = None # to store image_marker_coord at last frame
    image_ball_radius = None  #Image coordinate of balls center; Image plane Origin: Leftup cornor
    
    Cvector = None #vector of balls center to camera (System coordinate) in one frame
    
    ball_move_range_2d = 100 #ball center move range in image plane +- (pixel/s)
    ball_move_range_2d_current = None # = dt * ball_move_range_2d (ball center move range between two frames) 
    
    
class camera_info:
    num_cam = 4  #camera number
    num_marker = None  #ball number
    
    cam = [camera_info_definition(),camera_info_definition(),camera_info_definition(),camera_info_definition()]
    
    
    def __init__(self): # Info Import constructor
        for idx_cam in range(self.num_cam):
            
            self.cam[idx_cam].P_chess = info_P_chess[(idx_cam):(idx_cam+1),0:3]
            self.cam[idx_cam].R_chess = info_R_chess[(3*idx_cam):(3*idx_cam+3),0:3]
            
            self.cam[idx_cam].P_cam2chess = np.squeeze(info_P_cam2chess[(idx_cam):(idx_cam+1),0:3])
            self.cam[idx_cam].R_cam2chess = info_R_cam2chess[(3*idx_cam):(3*idx_cam+3),0:3]
            
            self.cam[idx_cam].P_cam = info_P_cam[(idx_cam):(idx_cam+1),0:3]
            self.cam[idx_cam].R_cam = info_R_cam[(3*idx_cam):(3*idx_cam+3),0:3]
            print(idx_cam)
            
#            if (idx_cam == 0):
#                self.cam[idx_cam].image_marker_coord = info_cam0_marker
#            elif (idx_cam == 1):
#                self.cam[idx_cam].image_marker_coord = info_cam1_marker
#            elif (idx_cam == 2):
#                self.cam[idx_cam].image_marker_coord = info_cam2_marker
#            elif (idx_cam == 3):
#                self.cam[idx_cam].image_marker_coord = info_cam3_marker
            
#            self.num_marker = info_cam0_marker.shape[0]
#            self.cam[idx_cam].Cvector = self.projection_vector(self.cam[idx_cam].R_cam,self.cam[idx_cam].image_marker_coord,self.cam[idx_cam].resolution,self.cam[idx_cam].ps,self.cam[idx_cam].f)
            
            #for idx_marker in range(self.num_marker):
            #self.cam[idx_cam].Cvector[idx_marker,0:3] = projection_vector(self,R_cam,image_marker_coord,resolution,ps,f)
            
    def projection_vector(self,R_cam,image_marker_coord,resolution,ps,f):
        vector = np.zeros((self.num_marker,3)) 
        for idx_marker in range(self.num_marker):
            center = np.squeeze(image_marker_coord[idx_marker,0:2])
            vector[idx_marker,0:3] = np.dot(R_cam,np.array([(center[0]-resolution[0][0]/2)*ps,(center[1]-resolution[0][1]/2)*ps,f]))
        return vector

    def point_between_2lines(self,Q1,Q2,q1,q2):
        Q21 = Q2-Q1;
        M = np.cross(q2,q1);
        m2 = np.dot(M,M);
        R = np.cross(Q21,M/m2);
        center = (Q1+np.dot(R,q2)*q1+Q2+np.dot(R,q1)*q2)/2;
        return center
    
    def center_calculator(self,idx_marker):
        center01 = self.point_between_2lines(self.cam[0].P_cam,self.cam[1].P_cam,self.cam[0].Cvector[idx_marker],self.cam[1].Cvector[idx_marker])
        center23 = self.point_between_2lines(self.cam[3].P_cam,self.cam[2].P_cam,self.cam[3].Cvector[idx_marker],self.cam[2].Cvector[idx_marker])
        center = (center01+center23)/2    
             
        return center        

ctest = camera_info()
    
#test_set = [2,3,6,7,8,9,12,13]           
for idx_cam in range(ctest.num_cam):
    if (idx_cam == 0):
        ctest.cam[idx_cam].image_marker_coord = info_cam0_marker
    elif (idx_cam == 1):
        ctest.cam[idx_cam].image_marker_coord = info_cam1_marker
    elif (idx_cam == 2):
        ctest.cam[idx_cam].image_marker_coord = info_cam2_marker
    elif (idx_cam == 3):
        ctest.cam[idx_cam].image_marker_coord = info_cam3_marker
    marker_select =  info_cam0_marker 
    ctest.num_marker = marker_select.shape[0]
    print(ctest.num_marker)
    ctest.cam[idx_cam].Cvector = ctest.projection_vector(ctest.cam[idx_cam].R_cam,ctest.cam[idx_cam].image_marker_coord,ctest.cam[idx_cam].resolution,ctest.cam[idx_cam].ps,ctest.cam[idx_cam].f)
 
for i in range(16):
    center = ctest.center_calculator(i)
    print(center)
