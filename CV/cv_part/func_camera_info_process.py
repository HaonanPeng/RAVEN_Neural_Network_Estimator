import cv2
import math
import numpy as np
from multiprocessing.pool import ThreadPool
import func_circle_detect as f_cd



info_txt_path = 'Camera_Info_txt/'

info_P_chess = np.loadtxt(info_txt_path + 'info_P_chess.txt')
info_R_chess = np.loadtxt(info_txt_path + 'info_R_chess.txt')
info_P_cam2chess = np.loadtxt(info_txt_path + 'info_P_cam2chess.txt')
info_R_cam2chess = np.loadtxt(info_txt_path + 'info_R_cam2chess.txt')
info_P_cam = np.loadtxt(info_txt_path + 'info_P_cam.txt')
info_R_cam = np.loadtxt(info_txt_path + 'info_R_cam.txt')

circle_center_decay = 0.5

#showplot = 0


class camera_info_definition():
    resolution = np.array([[1280,720]])  #photo resolution
    f = 4 # focal length of the camera (mm)
    ps = f/1420 # Pixel size in real world 
    
    P_chess = np.array([[0,0,0]]) #Chessboard origin P_cam2chess in System Coordinate
    R_chess = np.array([[1.0,0,0],[0,1.0,0],[0,0,1.0]]) #Chessboard Rotation Matrix in System coordinate
    
    P_cam2chess = np.array([[0,0,0]]) # camera P_cam2chess in Chessboard Coordinate (from Matlab camera_localization_Chessboard.m)
    R_cam2chess = np.array([[1,0,0],[0,1,0],[0,0,1]]) # camera rotation (from Matlab camera_localization_Chessboard.m)
    
    P_cam = np.array([[0,0,0]]) #camera P_cam in System coordinate
    R_cam = np.array([[1,0,0],[0,1,0],[0,0,1]]) #camera Rotation Matrix in System coordinate
    
    img_ball_center = None  #Image coordinate of balls center
    img_ball_center_lastframe = None # to store img_ball_center at last frame
    img_ball_radius = None  #Image coordinate of balls center
    
    Cvector = None #vector of balls center to camera (System coordinate) in one frame

    circle_radius_threshold_decay = 0.75
    circle_radius_expand = 20.0 # ball moves per second, the reference radius expand rate  
    circle_radius_max = None  
    circle_radius_min = None
    
    ball_move_rate_img = None # = dt * ball_move_range_2d (ball center move rate in unit time on image) 

    ref_color = None
    
    

class camera_info:
    num_cam = 4  #camera number
    num_ball = 3  #ball number
    listBall_effCam = [[] for _ in range(num_ball)] # list of effective cam_frame of each ball 
    listBall_effCam_last = [[] for _ in range(num_ball)]
    show_plot = 0
    
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
            self.cam[idx_cam].img_ball_center = np.zeros((self.num_ball,2)) 
            self.cam[idx_cam].img_ball_center_lastframe = np.zeros((self.num_ball,2)) 
            self.cam[idx_cam].img_ball_radius = np.zeros(self.num_ball) 

            self.cam[idx_cam].circle_radius_max = np.zeros(self.num_ball) 
            self.cam[idx_cam].circle_radius_min = np.zeros(self.num_ball) 
            self.cam[idx_cam].ref_color = np.zeros((3,self.num_ball))

            self.cam[idx_cam].ball_move_rate_img = np.ones((1,self.num_ball))*100.0


    def ball_img_detect_locate(self, img_input_list, carve_sign = 0):   
        img_result_list = [None, None, None, None]
        self.listBall_effCam = [[] for _ in range(self.num_ball)] 
        # for idx_cam in range(self.num_cam):
        #     self.cam[idx_cam].img_ball_center, self.cam[idx_cam].img_ball_radius, img_result_list[idx_cam] = f_cd.circle_center_detect_single_ball (img_input_list[idx_cam], showplot, 
        #                                                                                                                                             self.cam[idx_cam].circle_radius_min, self.cam[idx_cam].circle_radius_max, 
        #                                                                                                                                             self.cam[idx_cam].ref_color, self.num_ball, idx_cam, 
        #                                                                                                                                             carve_sign, self.cam[idx_cam].img_ball_center_lastframe, self.cam[idx_cam].img_ball_radius)
        #     self.cam[idx_cam].Cvector = self.projection_vector(self.cam[idx_cam].R_cam,self.cam[idx_cam].img_ball_center,self.cam[idx_cam].resolution,self.cam[idx_cam].ps,self.cam[idx_cam].f)
        #     for idx_ball in range(self.num_ball):  
        #         if np.sum(self.cam[idx_cam].img_ball_center[idx_ball,:])!=0:
        #             self.listBall_effCam[idx_ball].extend([idx_cam]) 
        # return img_result_list

        #multi-thread version
        pool = ThreadPool(processes=4)
        async_result_0 = pool.apply_async(f_cd.circle_center_detect_single_ball, (img_input_list[0], self.show_plot,self.cam[0].circle_radius_min, self.cam[0].circle_radius_max,self.cam[0].ref_color, self.num_ball, 0,carve_sign, self.cam[0].img_ball_center_lastframe, self.cam[0].img_ball_radius))
        async_result_1 = pool.apply_async(f_cd.circle_center_detect_single_ball, (img_input_list[1], self.show_plot,self.cam[1].circle_radius_min, self.cam[1].circle_radius_max,self.cam[1].ref_color, self.num_ball, 1,carve_sign, self.cam[1].img_ball_center_lastframe, self.cam[1].img_ball_radius))
        async_result_2 = pool.apply_async(f_cd.circle_center_detect_single_ball, (img_input_list[2], self.show_plot,self.cam[2].circle_radius_min, self.cam[2].circle_radius_max,self.cam[2].ref_color, self.num_ball, 2,carve_sign, self.cam[2].img_ball_center_lastframe, self.cam[2].img_ball_radius))
        async_result_3 = pool.apply_async(f_cd.circle_center_detect_single_ball, (img_input_list[3], self.show_plot,self.cam[3].circle_radius_min, self.cam[3].circle_radius_max,self.cam[3].ref_color, self.num_ball, 3,carve_sign, self.cam[3].img_ball_center_lastframe, self.cam[3].img_ball_radius))
        self.cam[0].img_ball_center, self.cam[0].img_ball_radius, img_result_list[0] = async_result_0.get()
        self.cam[1].img_ball_center, self.cam[1].img_ball_radius, img_result_list[1] = async_result_1.get()
        self.cam[2].img_ball_center, self.cam[2].img_ball_radius, img_result_list[2] = async_result_2.get()
        self.cam[3].img_ball_center, self.cam[3].img_ball_radius, img_result_list[3] = async_result_3.get()
        
        for idx_cam in range(self.num_cam):                                                                                             
            self.cam[idx_cam].Cvector = self.projection_vector(self.cam[idx_cam].R_cam,self.cam[idx_cam].img_ball_center,self.cam[idx_cam].resolution,self.cam[idx_cam].ps,self.cam[idx_cam].f)
            for idx_ball in range(self.num_ball):  
                if np.sum(self.cam[idx_cam].img_ball_center[idx_ball,:])!=0:
                    self.listBall_effCam[idx_ball].extend([idx_cam]) 
        return img_result_list
         
    def ball_world_locate(self,listBall_effCam):
        ball_center = np.zeros((self.num_ball,3))
        for idx_ball in range(self.num_ball): 
            ball_center[idx_ball,0:3] = np.squeeze(self.center_calculator(idx_ball,listBall_effCam[idx_ball]))
        return ball_center

    def projection_vector(self,R_cam,img_ball_center,resolution,ps,f):
        Cvector = np.zeros((self.num_ball,3)) 
        for idx_ball in range(self.num_ball):
            center = np.squeeze(img_ball_center[idx_ball,0:2])
            Cvector[idx_ball,0:3] = np.dot(R_cam,np.array([(center[0]-resolution[0][0]/2)*ps,(center[1]-resolution[0][1]/2)*ps,f]))
        return Cvector
    

    def point_between_2lines(self,Q1,Q2,q1,q2):
        Q21 = Q2-Q1
        M = np.cross(q2,q1)
        m2 = np.dot(M,M)
        R = np.cross(Q21,M/m2)
        center = (Q1+np.dot(R,q2)*q1+Q2+np.dot(R,q1)*q2)/2
        return center
    
    
    def center_calculator(self,idx_ball,list_selected_cam):
#        print(len(list_selected_cam))
        _=1
        if len(list_selected_cam) == 2:
            center = self.point_between_2lines(self.cam[list_selected_cam[0]].P_cam,self.cam[list_selected_cam[1]].P_cam,self.cam[list_selected_cam[0]].Cvector[idx_ball],self.cam[list_selected_cam[1]].Cvector[idx_ball])
        
        elif len(list_selected_cam) == 3:   
            center01 = self.point_between_2lines(self.cam[list_selected_cam[0]].P_cam,self.cam[list_selected_cam[1]].P_cam,self.cam[list_selected_cam[0]].Cvector[idx_ball],self.cam[list_selected_cam[1]].Cvector[idx_ball])
            center02 = self.point_between_2lines(self.cam[list_selected_cam[0]].P_cam,self.cam[list_selected_cam[2]].P_cam,self.cam[list_selected_cam[0]].Cvector[idx_ball],self.cam[list_selected_cam[2]].Cvector[idx_ball])
            center12 = self.point_between_2lines(self.cam[list_selected_cam[1]].P_cam,self.cam[list_selected_cam[2]].P_cam,self.cam[list_selected_cam[1]].Cvector[idx_ball],self.cam[list_selected_cam[2]].Cvector[idx_ball])
            center = (center01+center02+center12)/3
            
        elif len(list_selected_cam) == 4:   
            center01 = self.point_between_2lines(self.cam[list_selected_cam[0]].P_cam,self.cam[list_selected_cam[1]].P_cam,self.cam[list_selected_cam[0]].Cvector[idx_ball],self.cam[list_selected_cam[1]].Cvector[idx_ball])
            center23 = self.point_between_2lines(self.cam[list_selected_cam[3]].P_cam,self.cam[list_selected_cam[2]].P_cam,self.cam[list_selected_cam[3]].Cvector[idx_ball],self.cam[list_selected_cam[2]].Cvector[idx_ball])
            center = (center01+center23)/2
        else:
            center = None
            
        # could be more photo added ....    
             
        return center
    
    def set_show_plot(self, signal):
        self.show_plot = signal
        return None



