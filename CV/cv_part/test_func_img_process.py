 
import func_img_process as f_ip
import time
import numpy as np

img_processor0 = f_ip.img_processor()

img_processor0.camera_info.cam[0].circle_radius_max = np.array([])
img_processor0.camera_info.cam[0].circle_radius_min = np.array([])
img_processor0.camera_info.cam[0].ball_move_rate_img = 30

img_processor0.camera_info.cam[1].circle_radius_max = np.array([])
img_processor0.camera_info.cam[1].circle_radius_min = np.array([])
img_processor0.camera_info.cam[1].ball_move_rate_img = 30

img_processor0.camera_info.cam[2].circle_radius_max = np.array([])
img_processor0.camera_info.cam[2].circle_radius_min = np.array([])
img_processor0.camera_info.cam[2].ball_move_rate_img = 45

img_processor0.camera_info.cam[3].circle_radius_max = np.array([])
img_processor0.camera_info.cam[3].circle_radius_min = np.array([])
img_processor0.camera_info.cam[3].ball_move_rate_img = 55

img_processor0.load_time_str()

t = time.time()

for iteration in range(0,100):
    img_processor0.find_next_idx()
    img_processor0.load_img()
    img_processor0.locate_ball(iteration)
    img_processor0.save_img()
    img_processor0.show_cam_info()
    print(img_processor0.camera_info.cam[0].img_ball_radius)
    a = 1

elapsed = time.time() - t
print('\n\n time =',elapsed)    