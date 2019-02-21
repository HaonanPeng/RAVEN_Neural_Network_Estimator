import cv2
import math
import numpy as np
import time
import func_camera_info_process

# Main part of image processing
class img_processor:
    
    # Data files path
    bagfile_folder_path = "bagfiles/"
    cam0_folder_path = bagfile_folder_path + "img_camera0/"
    cam1_folder_path = bagfile_folder_path + "img_camera1/"
    cam2_folder_path = bagfile_folder_path + "img_camera2/"
    cam3_folder_path = bagfile_folder_path + "img_camera3/"
    cam0_time_str_path = cam0_folder_path + "time_stemp_camera0.txt"
    cam1_time_str_path = cam1_folder_path + "time_stemp_camera1.txt"
    cam2_time_str_path = cam2_folder_path + "time_stemp_camera2.txt"
    cam3_time_str_path = cam3_folder_path + "time_stemp_camera3.txt"
    raven_data_path = cam3_folder_path + "time_stemp_camera3.txt"
#    raven_data_path = bagfile_folder_path + "turtle_sim_state.txt"
    selected_frames_path = bagfile_folder_path + "selected_frames/"
    
    # Time stamps
    # For this and following defination, [0-3] means 4 cameras, and [4] means raven 
    time_str_vec = None
    
    # Current index
    idx_cur = [0,0,0,0,0]
    
    # Current time stamp
    time_str_cur = np.zeros(5)
    
    # Last effective camera time stamp
    time_eff_frame = np.zeros(4)

    # Current image
    img_cur = [None, None, None, None]
    
    # Current RAVEN state
    raven_state_cur = None
    
    # Frame counter
    frame_counter = 0
    
    # Result matrix
    result_matrix = np.zeros((1, 8))
    
    # camera info class initalization  
    camera_info = func_camera_info_process.camera_info()
    
    #ball center coordinate
    ball_center = np.zeros((3,3))
    
    #ball center move range in system coordinate +- (mm/s)
    ball_move_range_3d = 20
    
    

    # Load the time stamps and set initial values         
    def load_time_str(self):
        cam0_time_str_vec = np.loadtxt(self.cam0_time_str_path)
        cam1_time_str_vec = np.loadtxt(self.cam1_time_str_path)
        cam2_time_str_vec = np.loadtxt(self.cam2_time_str_path)
        cam3_time_str_vec = np.loadtxt(self.cam3_time_str_path)
        raven_time_str_vec = np.loadtxt(self.raven_data_path)
        
        max_len = max(np.size(cam0_time_str_vec),np.size(cam1_time_str_vec),np.size(cam2_time_str_vec),np.size(cam3_time_str_vec),np.size(raven_time_str_vec))
        self.time_str_vec = np.zeros((5,max_len))
        self.time_str_vec[0][0:np.size(cam0_time_str_vec)] = cam0_time_str_vec
        self.time_str_vec[1][0:np.size(cam1_time_str_vec)] = cam1_time_str_vec
        self.time_str_vec[2][0:np.size(cam2_time_str_vec)] = cam2_time_str_vec
        self.time_str_vec[3][0:np.size(cam3_time_str_vec)] = cam3_time_str_vec
        self.time_str_vec[4][0:np.size(raven_time_str_vec)] = raven_time_str_vec.reshape(max_len)
        print("[IMG_PROCESSOR]:Time stamps loaded")
        
        self.idx_cur = [0,0,0,0,0]
        print("[IMG_PROCESSOR]:Index initialized")
        
        self.time_str_cur[0] = self.time_str_vec[0][int(self.idx_cur[0])]
        self.time_str_cur[1] = self.time_str_vec[1][int(self.idx_cur[1])]
        self.time_str_cur[2] = self.time_str_vec[2][int(self.idx_cur[2])]
        self.time_str_cur[3] = self.time_str_vec[3][int(self.idx_cur[3])]
        self.time_str_cur[4] = self.time_str_vec[4][int(self.idx_cur[4])]
        print ("[IMG_PROCESSOR]:Current time stamp initialized")
        self.show_idx_time()
        
        for idx_cam in range(self.camera_info.num_cam):
            self.time_eff_frame[idx_cam] = self.time_str_cur[idx_cam]
        
        end_signal = 0
        
        return end_signal

    # This function is to find the next closest indice 
    def find_next_idx(self):
        time_str_nxt = np.array([self.time_str_vec[0][self.idx_cur[0]+1], self.time_str_vec[1][self.idx_cur[1]+1], self.time_str_vec[2][self.idx_cur[2]+1], self.time_str_vec[3][self.idx_cur[3]+1], self.time_str_vec[4][self.idx_cur[4]+1]])
        max_device = np.argmax(time_str_nxt)
        
        other_device = np.delete(np.array([0,1,2,3,4]), max_device)
        
        self.idx_cur[max_device] = self.idx_cur[max_device] + 1
        self.time_str_cur[max_device] = time_str_nxt[max_device]
        
        for i in other_device:
            self.idx_cur[i] = find_nearest(self.time_str_vec[i] , self.time_str_cur[max_device])
            self.time_str_cur[i] = self.time_str_vec[i][self.idx_cur[i]]
            
        self.frame_counter = self.frame_counter + 1
        print ("[IMG_PROCESSOR]:New index and time stamp are set:")    
        self.show_idx_time()
            
    # Function to load images relative to current time stamp
    def load_img(self):
        # Load cam0
        self.img_cur[0] = cv2.imread(self.cam0_folder_path + str("%.6f" % self.time_str_cur[0]) + ".jpg")
        # Load cam1
        self.img_cur[1] = cv2.imread(self.cam1_folder_path + str("%.6f" % self.time_str_cur[1]) + ".jpg")
        # Load cam2
        self.img_cur[2] = cv2.imread(self.cam2_folder_path + str("%.6f" % self.time_str_cur[2]) + ".jpg")
        # Load cam3
        self.img_cur[3] = cv2.imread(self.cam3_folder_path + str("%.6f" % self.time_str_cur[3]) + ".jpg")
        
    def locate_ball(self,index_iteration):
        
        # update the reference_radius_max/min with time range between current and last effective one  
        for idx_cam in range(self.camera_info.num_cam):
            dt = self.time_str_cur[idx_cam]-self.time_eff_frame[idx_cam] # delta time step 
            # updat reference circle radius
            self.camera_info.cam[idx_cam].circle_radius_max = dt*self.camera_info.cam[idx_cam].circle_radius_expand+self.camera_info.cam[idx_cam].circle_radius_max
            self.camera_info.cam[idx_cam].circle_radius_min = -dt*self.camera_info.cam[idx_cam].circle_radius_expand+self.camera_info.cam[idx_cam].circle_radius_min
            
            # update current reasonable 2d move range of the ball (on image)
            self.camera_info.cam[idx_cam].ball_move_range_2d_current = dt* self.camera_info.cam[idx_cam].ball_move_range_2d
            
     
        # detect and locate the ball center    
        temp_ball_center, self.img_cur, self.camera_info.eff_cam_num = self.camera_info.detect_locate(self.img_cur)
        
        # flag to indicate wether current image_ball_center is in reasonable range or not, default: YES 
        move_range_2d_pass = 1 
         
        # verify if the ball center 2D movement (effective frames) is in reasonable range
        if index_iteration != 0: 
            for i in range(len(self.camera_info.eff_cam_num)):
                idx_cam = int(self.camera_info.eff_cam_num[i])
                for idx_ball in range(self.camera_info.num_ball):
                    ball_center_current = self.camera_info.cam[idx_cam].image_ball_center[idx_ball]
                    ball_center_lastframe = self.camera_info.cam[idx_cam].image_ball_center_lastframe[idx_ball]
                    move_distance_2d = np.linalg.norm(ball_center_current - ball_center_lastframe)
                    
                    if move_distance_2d>self.camera_info.cam[idx_cam].ball_move_range_2d_current:
                        move_range_2d_pass = 0
                        print('[Warning]:','cam',idx_cam,' ball',idx_ball, 'moves', move_distance_2d, '(pixels), out of reasonable 2d range\n')                             
        
        if move_range_2d_pass == 0:
            print('[Failure]:ball moves out of reasonable 2d range')
            print('\n\n')
            
            # time step the ball update fails, roll back reference_radius_max/min
            for idx_cam in range(self.camera_info.num_cam):
                dt = self.time_str_cur[idx_cam]-self.time_eff_frame[idx_cam] # delta time step 
                self.camera_info.cam[idx_cam].circle_radius_max = -dt*self.camera_info.cam[idx_cam].circle_radius_expand+self.camera_info.cam[idx_cam].circle_radius_max
                self.camera_info.cam[idx_cam].circle_radius_min = dt*self.camera_info.cam[idx_cam].circle_radius_expand+self.camera_info.cam[idx_cam].circle_radius_min
            return 
        
        if len(self.camera_info.eff_cam_num)<=1:
            print('[Failure]:not enough effective frame to locate the ball\n\n')
            
            # time step the ball update fails, roll back reference_radius_max/min
            for idx_cam in range(self.camera_info.num_cam):
                dt = self.time_str_cur[idx_cam]-self.time_eff_frame[idx_cam] # delta time step 
                self.camera_info.cam[idx_cam].circle_radius_max = -dt*self.camera_info.cam[idx_cam].circle_radius_expand+self.camera_info.cam[idx_cam].circle_radius_max
                self.camera_info.cam[idx_cam].circle_radius_min = dt*self.camera_info.cam[idx_cam].circle_radius_expand+self.camera_info.cam[idx_cam].circle_radius_min
            return 
            return
        
        self.ball_center = temp_ball_center 
        print('[Success]:ball_center updated:\n',self.ball_center,'\n\n')
        
        #update the cam with effective frame time stamp 
        
        for i in range(len(self.camera_info.eff_cam_num)):
            idx_cam = int(self.camera_info.eff_cam_num[i])
            self.time_eff_frame[idx_cam] =  self.time_str_cur[idx_cam]
            
            # save the image_ball_center from last frame
            self.camera_info.cam[idx_cam].image_ball_center_lastframe = self.camera_info.cam[idx_cam].image_ball_center
        
        # roll back reference radius of uneffective frames
        full_cam_num = list(range(0,self.camera_info.num_cam))
        uneff_cam_num = [x for x in full_cam_num if x not in self.camera_info.eff_cam_num]
        
        for i in range(len(uneff_cam_num)):
            idx_cam = int(uneff_cam_num[i])
            dt = self.time_str_cur[idx_cam]-self.time_eff_frame[idx_cam] # delta time step 
            self.camera_info.cam[idx_cam].circle_radius_max = -dt*self.camera_info.cam[idx_cam].circle_radius_expand+self.camera_info.cam[idx_cam].circle_radius_max
            self.camera_info.cam[idx_cam].circle_radius_min = dt*self.camera_info.cam[idx_cam].circle_radius_expand+self.camera_info.cam[idx_cam].circle_radius_min


    def save_img(self):
        # Save cam0
        cam0_name = self.selected_frames_path + "frame_" + str(self.frame_counter) + "_cam0_time_" + str(self.time_str_cur[0]) + "_index_" + str(self.idx_cur[0]) + ".jpg"
        cv2.imwrite (cam0_name, self.img_cur[0])
        # Save cam1
        cam1_name = self.selected_frames_path + "frame_" + str(self.frame_counter) + "_cam1_time_" + str(self.time_str_cur[1]) + "_index_" + str(self.idx_cur[1]) + ".jpg"
        cv2.imwrite (cam1_name, self.img_cur[1])
        # Save cam2
        cam2_name = self.selected_frames_path + "frame_" + str(self.frame_counter) + "_cam2_time_" + str(self.time_str_cur[2]) + "_index_" + str(self.idx_cur[2]) + ".jpg"
        cv2.imwrite (cam2_name, self.img_cur[2])
        # Save cam3
        cam3_name = self.selected_frames_path + "frame_" + str(self.frame_counter) + "_cam3_time_" + str(self.time_str_cur[3]) + "_index_" + str(self.idx_cur[3]) + ".jpg"
        cv2.imwrite (cam3_name, self.img_cur[3])
        
    def show_idx_time(self):
        print ("___________________________________________________________")
        print ("[IMG_PROCESSOR]:Frame counter: " + str(self.frame_counter))

        print ("[IMG_PROCESSOR]:camera0 time stamp: " + str(self.time_str_cur[0]))
        print ("[IMG_PROCESSOR]:camera1 time stamp: " + str(self.time_str_cur[1]))
        print ("[IMG_PROCESSOR]:camera2 time stamp: " + str(self.time_str_cur[2]))
        print ("[IMG_PROCESSOR]:camera3 time stamp: " + str(self.time_str_cur[3]))
        print ("[IMG_PROCESSOR]:RAVEN time stamp:   " + str(self.time_str_cur[4]))
        print ("---------------------------------------------------")
        print ("[IMG_PROCESSOR]:camera0 index: " + str(self.idx_cur[0]))
        print ("[IMG_PROCESSOR]:camera1 index: " + str(self.idx_cur[1]))
        print ("[IMG_PROCESSOR]:camera2 index: " + str(self.idx_cur[2]))
        print ("[IMG_PROCESSOR]:camera3 index: " + str(self.idx_cur[3]))
        print ("[IMG_PROCESSOR]:RAVEN index:   " + str(self.idx_cur[4]))
        print ("---------------------------------------------------")
        
        
    def update_result(self, ball_center):
        self.result_matrix[self.frame_counter][0] = self.frame_counter
        self.result_matrix[self.frame_counter][1] = np.sum(self.time_str_cur) / 4
        
        i = 2
        for ball in ball_center:
            for value in ball:
                self.result_matrix[self.frame_counter][i] = value
                i = i + 1
                

# Commenly tool functions

# This is a function to find the nearest value 
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx
    

        
        
        
        
    