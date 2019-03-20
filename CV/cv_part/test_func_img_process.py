 
import func_img_process as f_ip
import time
import numpy as np

img_processor0 = f_ip.img_processor()

img_processor0.camera_info.cam[0].circle_radius_max = np.array([54,58,59])
img_processor0.camera_info.cam[0].circle_radius_min = np.array([52,56,57])
img_processor0.camera_info.cam[0].ball_move_rate_img = 30
img_processor0.camera_info.cam[0].ref_color = np.array([[80,130,50],[60,120,170],[100,60,160]]) 

img_processor0.camera_info.cam[1].circle_radius_max = np.array([47,51,54])
img_processor0.camera_info.cam[1].circle_radius_min = np.array([45,49,52])
img_processor0.camera_info.cam[1].ball_move_rate_img = 30
img_processor0.camera_info.cam[1].ref_color = np.array([[80,130,50],[60,120,170],[100,60,160]]) 

img_processor0.camera_info.cam[2].circle_radius_max = np.array([82,83,74])
img_processor0.camera_info.cam[2].circle_radius_min = np.array([80,81,72])
img_processor0.camera_info.cam[2].ball_move_rate_img = 45
img_processor0.camera_info.cam[2].ref_color = np.array([[150,210,90],[110,210,170],[170,80,170]]) 

img_processor0.camera_info.cam[3].circle_radius_max = np.array([63,68,67])
img_processor0.camera_info.cam[3].circle_radius_min = np.array([61,66,65])
img_processor0.camera_info.cam[3].ball_move_rate_img = 40
img_processor0.camera_info.cam[3].ref_color = np.array([[150,210,90],[110,210,170],[170,80,170]]) 

img_processor0.load_time_str()

t = time.time()

for iteration in range(0,150):
    img_processor0.find_next_idx()
    img_processor0.load_img()
    img_processor0.locate_ball(iteration)
    img_processor0.save_img()
    img_processor0.show_cam_info()

elapsed = time.time() - t
print('\n\n time =',elapsed)    