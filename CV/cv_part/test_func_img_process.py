import func_img_process as f_ip
import time
import numpy as np

img_processor0 = f_ip.img_processor()

# traj 1
# img_processor0.camera_info.cam[0].circle_radius_max = np.array([54,57,58])
# img_processor0.camera_info.cam[0].circle_radius_min = np.array([52,55,56])
# img_processor0.camera_info.cam[1].circle_radius_max = np.array([47,50,54])
# img_processor0.camera_info.cam[1].circle_radius_min = np.array([45,48,52])  
# img_processor0.camera_info.cam[2].circle_radius_max = np.array([82,84,76])
# img_processor0.camera_info.cam[2].circle_radius_min = np.array([80,82,74])
# img_processor0.camera_info.cam[3].circle_radius_max = np.array([66,68,68])
# img_processor0.camera_info.cam[3].circle_radius_min = np.array([63,66,66])

# traj 2
# img_processor0.camera_info.cam[0].circle_radius_max = np.array([58.0,62.0,60.0])
# img_processor0.camera_info.cam[0].circle_radius_min = np.array([54.0,57.0,56.0])
# img_processor0.camera_info.cam[1].circle_radius_max = np.array([50.0,55.0,58.0])
# img_processor0.camera_info.cam[1].circle_radius_min = np.array([46.0,50.0,53.0]) 
# img_processor0.camera_info.cam[2].circle_radius_max = np.array([80.0,80.0,78.0])
# img_processor0.camera_info.cam[2].circle_radius_min = np.array([74.0,75.0,72.0])
# img_processor0.camera_info.cam[3].circle_radius_max = np.array([63.0,67.0,69.0])
# img_processor0.camera_info.cam[3].circle_radius_min = np.array([59.0,62.0,64.0])

# traj 3
img_processor0.camera_info.cam[0].circle_radius_max = np.array([58.0,67.0,65.0])
img_processor0.camera_info.cam[0].circle_radius_min = np.array([54.0,63.0,61.0])
img_processor0.camera_info.cam[1].circle_radius_max = np.array([54.0,56.0,60.0])
img_processor0.camera_info.cam[1].circle_radius_min = np.array([50.0,52.0,55.0]) 
img_processor0.camera_info.cam[2].circle_radius_max = np.array([80.0,80.0,76.0])
img_processor0.camera_info.cam[2].circle_radius_min = np.array([74.0,75.0,72.0])
img_processor0.camera_info.cam[3].circle_radius_max = np.array([61.0,63.0,61.0])
img_processor0.camera_info.cam[3].circle_radius_min = np.array([57.0,59.0,57.0])

img_processor0.camera_info.cam[0].ball_move_rate_img = img_processor0.camera_info.cam[0].circle_radius_max*2            
img_processor0.camera_info.cam[1].ball_move_rate_img = img_processor0.camera_info.cam[1].circle_radius_max*2
img_processor0.camera_info.cam[2].ball_move_rate_img = img_processor0.camera_info.cam[2].circle_radius_max*2
img_processor0.camera_info.cam[3].ball_move_rate_img = img_processor0.camera_info.cam[3].circle_radius_max*2

img_processor0.load_time_str()

t = time.time()

for iteration in range(0,12000):
    img_processor0.find_next_idx()
    img_processor0.load_img()
    img_processor0.locate_ball(iteration)
    img_processor0.save_img()
    img_processor0.show_cam_info()
    img_processor0.update_result()


elapsed = time.time() - t
print('\n\n time =',elapsed)    