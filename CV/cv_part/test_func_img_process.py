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

# # traj 3
# img_processor0.camera_info.cam[0].circle_radius_max = np.array([58.0,67.0,65.0])
# img_processor0.camera_info.cam[0].circle_radius_min = np.array([54.0,63.0,61.0])
# img_processor0.camera_info.cam[1].circle_radius_max = np.array([54.0,56.0,60.0])
# img_processor0.camera_info.cam[1].circle_radius_min = np.array([50.0,52.0,55.0]) 
# img_processor0.camera_info.cam[2].circle_radius_max = np.array([80.0,80.0,76.0])
# img_processor0.camera_info.cam[2].circle_radius_min = np.array([74.0,75.0,72.0])
# img_processor0.camera_info.cam[3].circle_radius_max = np.array([61.0,63.0,61.0])
# img_processor0.camera_info.cam[3].circle_radius_min = np.array([57.0,59.0,57.0])

# traj 7
img_processor0.camera_info.cam[0].circle_radius_max = np.array([63.28949717, 65.69660177, 61.08359158])
img_processor0.camera_info.cam[0].circle_radius_min = np.array([51.8723274,  54.279432,   49.66642181])
img_processor0.camera_info.cam[1].circle_radius_max = np.array([59.84567117, 59.56068365, 53.04646196])
img_processor0.camera_info.cam[1].circle_radius_min = np.array([48.02584686, 47.74085934, 41.22663765]) 
img_processor0.camera_info.cam[2].circle_radius_max = np.array([73.07176994, 76.50223793, 73.68752711])
img_processor0.camera_info.cam[2].circle_radius_min = np.array([62.66895191, 66.0994199,  63.28470908])
img_processor0.camera_info.cam[3].circle_radius_max = np.array([67.10694289, 66.02487024, 65.8672883])
img_processor0.camera_info.cam[3].circle_radius_min = np.array([56.08483032, 55.00275767, 54.84517574])

# traj 8
#img_processor0.camera_info.cam[0].circle_radius_max = np.array([61.70054089, 63.01564551, 57.90062209])
#img_processor0.camera_info.cam[0].circle_radius_min = np.array([51.77729758, 53.0924022,  47.97737878])
#img_processor0.camera_info.cam[1].circle_radius_max = np.array([57.72862287, 57.26873507, 50.38933635])
#img_processor0.camera_info.cam[1].circle_radius_min = np.array([47.22068065, 46.76079285, 39.88139413]) 
#img_processor0.camera_info.cam[2].circle_radius_max = np.array([72.35911589, 76.10972434, 69.3097952])
#img_processor0.camera_info.cam[2].circle_radius_min = np.array([62.54095844, 66.29156689, 59.49163775])
#img_processor0.camera_info.cam[3].circle_radius_max = np.array([66.57824442, 64.98267861, 61.35150067])
#img_processor0.camera_info.cam[3].circle_radius_min = np.array([55.38583543, 53.79026963, 50.15909168])

# traj 9
#img_processor0.camera_info.cam[0].circle_radius_max = np.array([62.5289802,  62.53941639, 57.47400609])
#img_processor0.camera_info.cam[0].circle_radius_min = np.array([50.83629181, 50.84355679, 45.77814649])
#img_processor0.camera_info.cam[1].circle_radius_max = np.array([60.56627462, 57.64846012, 52.049225])
#img_processor0.camera_info.cam[1].circle_radius_min = np.array([50.26390197, 47.34608747, 41.66757205]) 
#img_processor0.camera_info.cam[2].circle_radius_max = np.array([82.12134807, 88.16707444, 79.7126857])
#img_processor0.camera_info.cam[2].circle_radius_min = np.array([70.0749771,  76.15875802, 67.7202])
#img_processor0.camera_info.cam[3].circle_radius_max = np.array([75.06330904, 80.8832811,  70.44936785])
#img_processor0.camera_info.cam[3].circle_radius_min = np.array([64.03393481, 55.71185343, 59.41999361])

# traj 11
#img_processor0.camera_info.cam[0].circle_radius_max = np.array([66.0,66.0,62.0])
#img_processor0.camera_info.cam[0].circle_radius_min = np.array([55.0,54.0,50.0])
#img_processor0.camera_info.cam[1].circle_radius_max = np.array([60.0,60.0,77.0])
#img_processor0.camera_info.cam[1].circle_radius_min = np.array([48.0,48.0,40.0]) 
#img_processor0.camera_info.cam[2].circle_radius_max = np.array([67.0,77.0,77.0])
#img_processor0.camera_info.cam[2].circle_radius_min = np.array([42.0,64.0,69.0])
#img_processor0.camera_info.cam[3].circle_radius_max = np.array([65.0,69.0,68.0])
#img_processor0.camera_info.cam[3].circle_radius_min = np.array([55.0,59.0,58.0])


img_processor0.camera_info.cam[0].ball_move_rate_img = img_processor0.camera_info.cam[0].circle_radius_max*2            
img_processor0.camera_info.cam[1].ball_move_rate_img = img_processor0.camera_info.cam[1].circle_radius_max*2
img_processor0.camera_info.cam[2].ball_move_rate_img = img_processor0.camera_info.cam[2].circle_radius_max*2
img_processor0.camera_info.cam[3].ball_move_rate_img = img_processor0.camera_info.cam[3].circle_radius_max*2

img_processor0.load_time_str()

t = time.time()

for iteration in range(0,50000):
    if iteration == 500:
        a = 1
        
    img_processor0.find_next_idx()
    img_processor0.load_img()
    img_processor0.locate_ball(iteration)
    img_processor0.save_img()
    img_processor0.show_cam_info()
    img_processor0.update_result()


elapsed = time.time() - t
print('\n\n time =',elapsed)    