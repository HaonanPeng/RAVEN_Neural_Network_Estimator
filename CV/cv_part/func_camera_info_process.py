import cv2
import math
import numpy as np
import func_circle_detect as f_cd


info_txt_path = 'camera_Info_txt/'

info_P_chess = np.loadtxt(info_txt_path + 'info_P_chess.txt')
info_R_chess = np.loadtxt(info_txt_path + 'info_R_chess.txt')
info_P_cam2chess = np.loadtxt(info_txt_path + 'info_P_cam2chess.txt')
info_R_cam2chess = np.loadtxt(info_txt_path + 'info_R_cam2chess.txt')
info_P_cam = np.loadtxt(info_txt_path + 'info_P_cam.txt')
info_R_cam = np.loadtxt(info_txt_path + 'info_R_cam.txt')


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
    
    image_ball_center = None  #Image coordinate of balls center; Image plane Origin: Leftup cornor
    image_ball_center_lastframe = None # to store image_ball_center at last frame
    image_ball_radius = None  #Image coordinate of balls center; Image plane Origin: Leftup cornor
    
    Cvector = None #vector of balls center to camera (System coordinate) in one frame

    circle_radius_threshold_decay = 0.8;
    circle_radius_expand = 3; # ball moves per second, the reference radius expand +- 3 pixel 
    circle_radius_max = 55  ;
    circle_radius_min = 30;   
    
    ball_move_range_2d = 100 #ball center move range in image plane +- (pixel/s)
    ball_move_range_2d_current = None # = dt * ball_move_range_2d (ball center move range between two frames) 
    
    
class camera_info:
    num_cam = 4  #camera number
    num_ball = 3  #ball number
    eff_cam_num = None # current cam with effective frame number - the frame in which the ball can be found  
    
    cam = [camera_info_definition(),camera_info_definition(),camera_info_definition(),camera_info_definition()]
    
    
    def __init__(self): # Info Import constructor
        for idx_cam in range(self.num_cam):
            self.cam[idx_cam].P_chess = info_P_chess[(idx_cam):(idx_cam+1),0:3]
            self.cam[idx_cam].R_chess = info_R_chess[(3*idx_cam):(3*idx_cam+3),0:3]
            
            self.cam[idx_cam].P_cam2chess = np.squeeze(info_P_cam2chess[(idx_cam):(idx_cam+1),0:3])
            self.cam[idx_cam].R_cam2chess = info_R_cam2chess[(3*idx_cam):(3*idx_cam+3),0:3]
            
            self.cam[idx_cam].P_cam = info_P_cam[(idx_cam):(idx_cam+1),0:3]
            self.cam[idx_cam].R_cam = info_R_cam[(3*idx_cam):(3*idx_cam+3),0:3]
            
            self.cam[idx_cam].Cvector = np.zeros((self.num_ball,3)) 
            self.cam[idx_cam].image_ball_center = np.zeros((self.num_ball,2)) 
            self.cam[idx_cam].image_ball_radius = np.zeros(self.num_ball) 
            
            
    def detect_locate(self,img_input_list):   
        self.eff_cam_num = np.array([])
        ball_center = np.zeros((self.num_ball,3))
        img_result_list = [None, None, None, None]
        
        for idx_cam in range(self.num_cam):
            self.cam[idx_cam].image_ball_center, self.cam[idx_cam].image_ball_radius, img_result_list[idx_cam] = f_cd.circle_center_detect (img_input_list[idx_cam], 1 , self.cam[idx_cam].circle_radius_min, self.cam[idx_cam].circle_radius_max)

            # all ballecs have been successfully detected 
            if np.sum(self.cam[idx_cam].image_ball_center)!=0:
                # add index into effective photo list
                self.eff_cam_num = np.concatenate((self.eff_cam_num,np.array([idx_cam]))) 
                self.cam[idx_cam].Cvector = self.projection_vector(self.cam[idx_cam].R_cam,self.cam[idx_cam].image_ball_center,self.cam[idx_cam].resolution,self.cam[idx_cam].ps,self.cam[idx_cam].f)
                
                self.cam[idx_cam].circle_radius_max = self.cam[idx_cam].circle_radius_threshold_decay*self.cam[idx_cam].circle_radius_max+(1-self.cam[idx_cam].circle_radius_threshold_decay)*np.max(self.cam[idx_cam].image_ball_radius)
                self.cam[idx_cam].circle_radius_min = self.cam[idx_cam].circle_radius_threshold_decay*self.cam[idx_cam].circle_radius_min+(1-self.cam[idx_cam].circle_radius_threshold_decay)*np.min(self.cam[idx_cam].image_ball_radius) 
        
         
        #less than 2 effective frame, the ball cannot be located
        if len(self.eff_cam_num)<=1:
            print('effective frame <=1, skip this time step\n')
            return None, img_result_list, self.eff_cam_num
        
#        self.eff_cam_num = self.eff_cam_num.astype(int)
        self.eff_cam_num = int(self.eff_cam_num)
        
        
        
        for idx_ball in range(self.num_ball): 
            ball_center[idx_ball,0:3] = np.squeeze(self.center_calculator(idx_ball)) 
        return ball_center, img_result_list, self.eff_cam_num


    def projection_vector(self,R_cam,image_ball_center,resolution,ps,f):
        Cvector = np.zeros((self.num_ball,3)) 
        for idx_ball in range(self.num_ball):
            center = np.squeeze(image_ball_center[idx_ball,0:2])
            Cvector[idx_ball,0:3] = np.dot(R_cam,np.array([(center[0]-resolution[0][0]/2)*ps,(center[1]-resolution[0][1]/2)*ps,f]))
        return Cvector
    

    def point_between_2lines(self,Q1,Q2,q1,q2):
        Q21 = Q2-Q1;
        M = np.cross(q2,q1);
        m2 = np.dot(M,M);
        R = np.cross(Q21,M/m2);
        center = (Q1+np.dot(R,q2)*q1+Q2+np.dot(R,q1)*q2)/2;
        return center
    
    
    def center_calculator(self,idx_ball):
        self.eff_cam_num = [2,3]
        if len(self.eff_cam_num) == 2:
            center = self.point_between_2lines(self.cam[self.eff_cam_num[0]].P_cam,self.cam[self.eff_cam_num[1]].P_cam,self.cam[self.eff_cam_num[0]].Cvector[idx_ball],self.cam[self.eff_cam_num[1]].Cvector[idx_ball])
        
        elif len(self.eff_cam_num) == 3:   
            center01 = self.point_between_2lines(self.cam[self.eff_cam_num[0]].P_cam,self.cam[self.eff_cam_num[1]].P_cam,self.cam[self.eff_cam_num[0]].Cvector[idx_ball],self.cam[self.eff_cam_num[1]].Cvector[idx_ball])
            center02 = self.point_between_2lines(self.cam[self.eff_cam_num[0]].P_cam,self.cam[self.eff_cam_num[2]].P_cam,self.cam[self.eff_cam_num[0]].Cvector[idx_ball],self.cam[self.eff_cam_num[2]].Cvector[idx_ball])
            center12 = self.point_between_2lines(self.cam[self.eff_cam_num[1]].P_cam,self.cam[self.eff_cam_num[2]].P_cam,self.cam[self.eff_cam_num[1]].Cvector[idx_ball],self.cam[self.eff_cam_num[2]].Cvector[idx_ball])
            center = (center01+center02+center12)/3
            
        elif len(self.eff_cam_num) == 4:   
            center01 = self.point_between_2lines(self.cam[self.eff_cam_num[0]].P_cam,self.cam[self.eff_cam_num[1]].P_cam,self.cam[self.eff_cam_num[0]].Cvector[idx_ball],self.cam[self.eff_cam_num[1]].Cvector[idx_ball])
            center23 = self.point_between_2lines(self.cam[self.eff_cam_num[3]].P_cam,self.cam[self.eff_cam_num[2]].P_cam,self.cam[self.eff_cam_num[3]].Cvector[idx_ball],self.cam[self.eff_cam_num[2]].Cvector[idx_ball])
            center = (center01+center23)/2    
            
        # could be more photo added ....    
             
        return center        






