import cv2
import math
import numpy as np
import time
import func_camera_info_process
import sys

# Main part of image processing
class img_processor:
    
    write_log = 1 # if 1, the console output will be write in to log file
    
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
    raven_data_path = bagfile_folder_path + "raven_state_time.txt"
    selected_frames_path = bagfile_folder_path + "selected_frames/"
    selected_frames_path_cam0 = bagfile_folder_path + "selected_frames_cam0/"
    selected_frames_path_cam1 = bagfile_folder_path + "selected_frames_cam1/"
    selected_frames_path_cam2 = bagfile_folder_path + "selected_frames_cam2/"
    selected_frames_path_cam3 = bagfile_folder_path + "selected_frames_cam3/"
    
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
    
    # Result matrix with: #frame, time, the center of three balls
    result_matrix = np.zeros((1, 11))
    
    # camera info class initalization  
    camera_info = func_camera_info_process.camera_info()
    
    #ball center coordinate
    ball_center = np.zeros((3,3))
    
    #ball center move range in system coordinate +- (mm/s)
    ball_move_range_3d = 20
    
    # signal indicating the first call
    first_call = 0
    
    # index seed, will be used in the filter
    idx_seed = None
    
    time_difference = 1.18 # This is the difference between the two computers, if the 4 webcams are connected to one computer, this should be 0
        

    # Load the time stamps and set initial values         
    def load_time_str(self):
        
        
        cam0_time_str_vec = np.loadtxt(self.cam0_time_str_path) + self.time_difference
        cam1_time_str_vec = np.loadtxt(self.cam1_time_str_path) + self.time_difference
        cam2_time_str_vec = np.loadtxt(self.cam2_time_str_path)
        cam3_time_str_vec = np.loadtxt(self.cam3_time_str_path)
        raven_time_str_vec = np.loadtxt(self.raven_data_path)
        
        max_len = max(np.size(cam0_time_str_vec),np.size(cam1_time_str_vec),np.size(cam2_time_str_vec),np.size(cam3_time_str_vec),np.size(raven_time_str_vec))
        self.time_str_vec = np.zeros((5,max_len))
        self.time_str_vec[0][0:np.size(cam0_time_str_vec)] = cam0_time_str_vec
        self.time_str_vec[1][0:np.size(cam1_time_str_vec)] = cam1_time_str_vec
        self.time_str_vec[2][0:np.size(cam2_time_str_vec)] = cam2_time_str_vec
        self.time_str_vec[3][0:np.size(cam3_time_str_vec)] = cam3_time_str_vec
        self.time_str_vec[4][0:np.size(raven_time_str_vec)] = raven_time_str_vec
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
        
        self.first_call = 0
        end_signal = 0
        
        if self.write_log == 1:
            log_file_name = self.bagfile_folder_path + "log_img_processor.log"
            print("[IMG_PROCESSOR]: Output is written into the log file: " + log_file_name)
            f_handler=open(log_file_name, 'w')
            sys.stdout=f_handler
        
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
        
        if self.first_call == 0:
            idx_cur_temp = self.idx_cur
            self.idx_seed = [idx_cur_temp]
            self.first_call = 1
        else:
            idx_cur_temp = self.idx_cur
            self.idx_seed = np.append(self.idx_seed, [idx_cur_temp], axis = 0)
            
        print ("[IMG_PROCESSOR]:New index and time stamp are set:")    
        self.show_idx_time()
            
    # Function to load images relative to current time stamp
    def load_img(self):
        # Load cam0
        self.img_cur[0] = cv2.imread(self.cam0_folder_path + str("%.6f" % (self.time_str_cur[0] - self.time_difference)) + ".jpg")
        # Load cam1
        self.img_cur[1] = cv2.imread(self.cam1_folder_path + str("%.6f" % (self.time_str_cur[1] - self.time_difference)) + ".jpg")
        # Load cam2
        self.img_cur[2] = cv2.imread(self.cam2_folder_path + str("%.6f" % self.time_str_cur[2]) + ".jpg")
        # Load cam3
        self.img_cur[3] = cv2.imread(self.cam3_folder_path + str("%.6f" % self.time_str_cur[3]) + ".jpg")
        
    def locate_ball(self,index_iteration):

        def update_ref_radius(list_cam_update):
            for i in range(len(list_cam_update)):
                idx_cam = int(list_cam_update[i])
                dt = self.time_str_cur[idx_cam]-self.time_eff_frame[idx_cam] # delta time step
                # updat reference circle radius
                for idx_ball in range(self.camera_info.num_ball): 
                    self.camera_info.cam[idx_cam].circle_radius_max[idx_ball] += dt*self.camera_info.cam[idx_cam].circle_radius_expand
                    self.camera_info.cam[idx_cam].circle_radius_min[idx_ball] -= dt*self.camera_info.cam[idx_cam].circle_radius_expand 
                
        def unupdate_ref_radius(list_cam_unupdate):
            for i in range(len(list_cam_unupdate)):
                idx_cam = int(list_cam_unupdate[i])
                dt = self.time_str_cur[idx_cam]-self.time_eff_frame[idx_cam] # delta time step 
                # updat reference circle radius
                for idx_ball in range(self.camera_info.num_ball): 
                    self.camera_info.cam[idx_cam].circle_radius_max[idx_ball] -= dt*self.camera_info.cam[idx_cam].circle_radius_expand
                    self.camera_info.cam[idx_cam].circle_radius_min[idx_ball] += dt*self.camera_info.cam[idx_cam].circle_radius_expand  



        # update the reference_radius_max/min with time range between current and last effective one 
        if index_iteration != 0:
            update_ref_radius(list(range(0,self.camera_info.num_cam)))

        # save the list of effective frame from last time    
        if index_iteration != 0:
            self.camera_info.list_eff_cam_last = self.camera_info.list_eff_cam

        # detect and locate the ball center on image, generate list of camera with effective frame
        self.img_cur = self.camera_info.ball_img_detect_locate(self.img_cur)
         
        # verify if the ball center 2D movement (effective frames) is in reasonable range
        if index_iteration != 0:
            #list to record the uneffective frame number  
            list_to_remove = [] 
            for i in range(len(self.camera_info.list_eff_cam)):
                idx_cam = self.camera_info.list_eff_cam[i]
                uneff_sign = 0  

                for idx_ball in range(self.camera_info.num_ball):

                    # calculate the ball center move distance between two frames  
                    # ball_center_current = self.camera_info.cam[idx_cam].img_ball_center[idx_ball]
                    # ball_center_lastframe = self.camera_info.cam[idx_cam].img_ball_center_lastframe[idx_ball]
                    # move_distance_2d = np.linalg.norm(ball_center_current - ball_center_lastframe)
                    
                    move_distance_2d = np.linalg.norm(self.camera_info.cam[idx_cam].img_ball_center[idx_ball] - self.camera_info.cam[idx_cam].img_ball_center_lastframe[idx_ball])
                    
                    # find if image move  
                    dt = self.time_str_cur[idx_cam]-self.time_eff_frame[idx_cam]
                    if move_distance_2d>(dt*self.camera_info.cam[idx_cam].ball_move_rate_img[idx_ball]):
                        uneff_sign = 1
                        print('[Warning]:','cam',idx_cam,' ball',idx_ball, 'moves', move_distance_2d, '(pixels), out of reasonable 2d range\n',dt*self.camera_info.cam[idx_cam].ball_move_rate_img)                             
                
                # if the current frame contains a ball out of range, remove this frame from list_eff_cam
                if uneff_sign == 1:                         
                    list_to_remove += [idx_cam]
            
            # remove uneffective camera frames
            self.camera_info.list_eff_cam = [x for x in self.camera_info.list_eff_cam if x not in list_to_remove]

            if len(self.camera_info.list_eff_cam)<=1:
                print('current effective frame <=1, system suspend\n')
                sys.exit(0)
        
        # generate the list of trusted frame  (effective in both last time and current time)
        list_cam_trust = [x for x in self.camera_info.list_eff_cam if x in self.camera_info.list_eff_cam_last] 
        
        if len(list_cam_trust)<=1:
            print('effective frame as reference <=1, system suspend\n')
            sys.exit(0)

        # generate the list of frame back to work (uneffective in last time, effective in current time)
        list_cam_new = [x for x in self.camera_info.list_eff_cam if x not in list_cam_trust]

        # calculate ball-center world coordinate from trust
        self.ball_center = self.camera_info.ball_world_locate(list_cam_trust)

        # verify if the back-to-work frame is effectve, yes then add 
        for i in range(len(list_cam_new)):
            idx_cam_new = list_cam_new[i]
            pass_sign = 1

            for j in range(len(list_cam_trust)):
                idx_cam_trust = list_cam_trust[j]
                temp_ball_center = self.camera_info.ball_world_locate([idx_cam_new,idx_cam_trust])
                ball_center_diff = np.linalg.norm(temp_ball_center-self.ball_center,axis=1)

                # fail if one of all balls out of range, 
                if np.any(ball_center_diff >= 10):
                    pass_sign = 0

            if pass_sign == 1:
                print('cam[',idx_cam_new,']back to work-----------------------------------')
                list_cam_trust.append(idx_cam_new)
        
        self.camera_info.list_eff_cam_last = list_cam_trust
        # recalculate the ball center 
        self.ball_center = self.camera_info.ball_world_locate(self.camera_info.list_eff_cam_last)
      
        print('[Success]:ball_center updated:\n',self.ball_center,'\n\n')
        
        #update the cam with effective frame time stamp 
        for i in range(len(self.camera_info.list_eff_cam)):
            idx_cam = self.camera_info.list_eff_cam[i]
            self.time_eff_frame[idx_cam] =  self.time_str_cur[idx_cam]
            # save the img_ball_center from last frame
            self.camera_info.cam[idx_cam].img_ball_center_lastframe = self.camera_info.cam[idx_cam].img_ball_center
            # update the ball_move_rate_img with the half of max image radius
            self.camera_info.cam[idx_cam].ball_move_rate_img = self.camera_info.cam[idx_cam].img_ball_radius
        
        list_uneff_cam = [x for x in list(range(0,self.camera_info.num_cam)) if x not in self.camera_info.list_eff_cam]
        # roll back reference radius of uneffective frames
        unupdate_ref_radius(list_uneff_cam)
        

    def save_img(self):
        # Save cam0
        cam0_name = self.selected_frames_path + "frame_" + str(self.frame_counter) + "_cam0_time_" + str(self.time_str_cur[0]) + "_index_" + str(self.idx_cur[0]) + ".jpg"
        cam0_name_n = self.selected_frames_path_cam0  + "frame_" + str(self.frame_counter) + "_cam0_time_" + str(self.time_str_cur[0]) + "_index_" + str(self.idx_cur[0]) + ".jpg"
        cv2.imwrite (cam0_name, self.img_cur[0])
        cv2.imwrite (cam0_name_n, self.img_cur[0])
        # Save cam1
        cam1_name = self.selected_frames_path + "frame_" + str(self.frame_counter) + "_cam1_time_" + str(self.time_str_cur[1]) + "_index_" + str(self.idx_cur[1]) + ".jpg"
        cam1_name_n = self.selected_frames_path_cam1 + "frame_" + str(self.frame_counter) + "_cam1_time_" + str(self.time_str_cur[1]) + "_index_" + str(self.idx_cur[1]) + ".jpg"
        cv2.imwrite (cam1_name, self.img_cur[1])
        cv2.imwrite (cam1_name_n, self.img_cur[1])
        # Save cam2
        cam2_name = self.selected_frames_path + "frame_" + str(self.frame_counter) + "_cam2_time_" + str(self.time_str_cur[2]) + "_index_" + str(self.idx_cur[2]) + ".jpg"
        cam2_name_n = self.selected_frames_path_cam2 + "frame_" + str(self.frame_counter) + "_cam2_time_" + str(self.time_str_cur[2]) + "_index_" + str(self.idx_cur[2]) + ".jpg"
        cv2.imwrite (cam2_name, self.img_cur[2])
        cv2.imwrite (cam2_name_n, self.img_cur[2])
        # Save cam3
        cam3_name = self.selected_frames_path + "frame_" + str(self.frame_counter) + "_cam3_time_" + str(self.time_str_cur[3]) + "_index_" + str(self.idx_cur[3]) + ".jpg"
        cam3_name_n = self.selected_frames_path_cam3 + "frame_" + str(self.frame_counter) + "_cam3_time_" + str(self.time_str_cur[3]) + "_index_" + str(self.idx_cur[3]) + ".jpg"
        cv2.imwrite (cam3_name, self.img_cur[3])
        cv2.imwrite (cam3_name_n, self.img_cur[3])
        
    def save_idx_seed(self):
        file_name = self.bagfile_folder_path + "idx_seed.txt"
        np.savetxt(file_name, self.idx_seed)
        
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
        
    def show_cam_info(self):
        print ("___________________________________________________________")
        print ("[IMG_PROCESSOR]:Frame counter: " + str(self.frame_counter))
        print ("---------------------------------------------------")
        print ("[IMG_PROCESSOR]:Cam0 MAX radius: " + str(self.camera_info.cam[0].circle_radius_max))
        print ("[IMG_PROCESSOR]:Cam0 MIN radius: " + str(self.camera_info.cam[0].circle_radius_min))
        print ("---------------------------------------------------")
        print ("[IMG_PROCESSOR]:Cam1 MAX radius: " + str(self.camera_info.cam[1].circle_radius_max))
        print ("[IMG_PROCESSOR]:Cam1 MIN radius: " + str(self.camera_info.cam[1].circle_radius_min))
        print ("---------------------------------------------------")
        print ("[IMG_PROCESSOR]:Cam2 MAX radius: " + str(self.camera_info.cam[2].circle_radius_max))
        print ("[IMG_PROCESSOR]:Cam2 MIN radius: " + str(self.camera_info.cam[2].circle_radius_min))
        print ("---------------------------------------------------")
        print ("[IMG_PROCESSOR]:Cam3 MAX radius: " + str(self.camera_info.cam[3].circle_radius_max))
        print ("[IMG_PROCESSOR]:Cam3 MIN radius: " + str(self.camera_info.cam[3].circle_radius_min))
        
    def update_result(self):
        self.result_matrix[0,0] = self.frame_counter
        # print(self.time_str_cur)
        
        self.result_matrix[0,1] = np.sum(self.time_str_cur)/5
        self.result_matrix[0,2:11] = self.ball_center.flatten()
        # print(self.result_matrix)
        if self.first_call_result_txt == 0:
            file=open('img_process_result.txt','w')
            np.savetxt(file, self.result_matrix, fmt='%.4f',delimiter='\t')
            file.close()
            self.first_call_result_txt = 1
        else:
            file=open('img_process_result.txt','ab')
            np.savetxt(file, self.result_matrix, fmt='%.4f',delimiter='\t')
            file.close()

        

# Commenly tool functions

# This is a function to find the nearest value 
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx