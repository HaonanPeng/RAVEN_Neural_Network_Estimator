 
import func_img_process as f_ip
import time
import numpy as np

img_processor0 = f_ip.img_processor()

# img_processor0.camera_info.cam[0].circle_radius_max = np.array([54,57,58])
# img_processor0.camera_info.cam[0].circle_radius_min = np.array([52,55,56])
img_processor0.camera_info.cam[0].circle_radius_max = np.array([55,58,59])
img_processor0.camera_info.cam[0].circle_radius_min = np.array([51,54,55])
img_processor0.camera_info.cam[0].ball_move_rate_img = img_processor0.camera_info.cam[0].circle_radius_max
img_processor0.camera_info.cam[0].ref_color = np.array([[80,130,50],[60,120,170],[100,60,160]]) 
 
# img_processor0.camera_info.cam[1].circle_radius_max = np.array([47,50,54])
# img_processor0.camera_info.cam[1].circle_radius_min = np.array([45,48,52])   
img_processor0.camera_info.cam[1].circle_radius_max = np.array([48,51,55])
img_processor0.camera_info.cam[1].circle_radius_min = np.array([44,47,51])                                       
img_processor0.camera_info.cam[1].ball_move_rate_img = img_processor0.camera_info.cam[1].circle_radius_max
img_processor0.camera_info.cam[1].ref_color = np.array([[80,130,50],[60,120,170],[100,60,160]]) 

# img_processor0.camera_info.cam[2].circle_radius_max = np.array([82,84,76])
# img_processor0.camera_info.cam[2].circle_radius_min = np.array([80,82,74])
img_processor0.camera_info.cam[2].circle_radius_max = np.array([84,86,78])
img_processor0.camera_info.cam[2].circle_radius_min = np.array([78,80,72])
img_processor0.camera_info.cam[2].ball_move_rate_img = img_processor0.camera_info.cam[2].circle_radius_max
img_processor0.camera_info.cam[2].ref_color = np.array([[150,210,90],[110,210,170],[170,80,170]]) 

# img_processor0.camera_info.cam[3].circle_radius_max = np.array([66,68,68])
# img_processor0.camera_info.cam[3].circle_radius_min = np.array([63,66,66])
img_processor0.camera_info.cam[3].circle_radius_max = np.array([68,70,70])
img_processor0.camera_info.cam[3].circle_radius_min = np.array([61,64,64])
img_processor0.camera_info.cam[3].ball_move_rate_img = img_processor0.camera_info.cam[3].circle_radius_max
img_processor0.camera_info.cam[3].ref_color = np.array([[150,210,90],[110,210,170],[170,80,170]]) 

img_processor0.load_time_str()

t = time.time()

for iteration in range(0,10000):
    img_processor0.find_next_idx()
    img_processor0.load_img()
    img_processor0.locate_ball(iteration)
    img_processor0.save_img()
    img_processor0.show_cam_info()
    img_processor0.update_result()


elapsed = time.time() - t
print('\n\n time =',elapsed)    