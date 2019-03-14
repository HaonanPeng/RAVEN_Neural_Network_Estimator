 
import func_img_process as f_ip
import time

img_processor0 = f_ip.img_processor()

img_processor0.camera_info.cam[0].circle_radius_max = 60
img_processor0.camera_info.cam[0].circle_radius_min = 45
img_processor0.camera_info.cam[0].min_center_distance = 90


img_processor0.camera_info.cam[1].circle_radius_max = 55
img_processor0.camera_info.cam[1].circle_radius_min = 40
img_processor0.camera_info.cam[1].min_center_distance = 75


img_processor0.camera_info.cam[2].circle_radius_max = 85
img_processor0.camera_info.cam[2].circle_radius_min = 60
img_processor0.camera_info.cam[2].min_center_distance = 125


img_processor0.camera_info.cam[3].circle_radius_max = 110
img_processor0.camera_info.cam[3].circle_radius_min = 60
img_processor0.camera_info.cam[3].min_center_distance = 100


img_processor0.load_time_str()


t = time.time()

for iteration in range(0,1000):
    img_processor0.find_next_idx()
    img_processor0.load_img()
    img_processor0.locate_ball(iteration)
    img_processor0.save_img()

elapsed = time.time() - t
print('\n\n time =',elapsed)    