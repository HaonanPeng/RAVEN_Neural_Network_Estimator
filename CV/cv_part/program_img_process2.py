import func_img_process as f_ip
import time
import numpy as np
import csv

img_processor0 = f_ip.img_processor()

img_processor0.set_write_log(1)
img_processor0.set_show_plot(0)
img_processor0.set_frame_jump(jump_type = 'auto' , 
                              move_range = 20 , 
                              auto_jump_frames = 5 , 
                              manual_jump_frames = None)

max_frames = 10000000

# traj 13
img_processor0.camera_info.cam[0].circle_radius_max = np.array([67.73304875, 72.24566054, 62.75119121])
img_processor0.camera_info.cam[0].circle_radius_min = np.array([55.93283322, 60.44544501, 50.95097568])
img_processor0.camera_info.cam[1].circle_radius_max = np.array([61.90296786, 62.28985789, 94.59773352])
img_processor0.camera_info.cam[1].circle_radius_min = np.array([50.50827124, 50.89516127, 39.75535056]) 
img_processor0.camera_info.cam[2].circle_radius_max = np.array([73.12972602, 81.68635139, 84.00631294])
img_processor0.camera_info.cam[2].circle_radius_min = np.array([62.13096672, 71.08659219, 73.819085  ])
img_processor0.camera_info.cam[3].circle_radius_max = np.array([66.29196674, 66.82141447, 69.7970318 ])
img_processor0.camera_info.cam[3].circle_radius_min = np.array([55.44509272, 55.97454045, 58.95015778])

# traj 14
#img_processor0.camera_info.cam[0].circle_radius_max = np.array([112.29271566,  65.32702392,  63.47352746])
#img_processor0.camera_info.cam[0].circle_radius_min = np.array([26.77334037, 55.53123237, 53.83255403])
#img_processor0.camera_info.cam[1].circle_radius_max = np.array([52.89808984, 60.08519026, 56.81488821])
#img_processor0.camera_info.cam[1].circle_radius_min = np.array([42.83945286, 50.02655327, 46.75625123]) 
#img_processor0.camera_info.cam[2].circle_radius_max = np.array([95.67482706,  87.20027223, 112.29271566])
#img_processor0.camera_info.cam[2].circle_radius_min = np.array([85.50043883, 77.025884,   26.77334037])
#img_processor0.camera_info.cam[3].circle_radius_max = np.array([76.4177672,  77.52155045, 67.34299403])
#img_processor0.camera_info.cam[3].circle_radius_min = np.array([65.9705074,  67.07429065, 56.89573423])

# traj test
#img_processor0.camera_info.cam[0].circle_radius_max = np.array([150.0, 150.0, 150.0])
#img_processor0.camera_info.cam[0].circle_radius_min = np.array([35.0,  35.0,   35.0])
#img_processor0.camera_info.cam[1].circle_radius_max = np.array([150.0, 150.0, 150.0])
#img_processor0.camera_info.cam[1].circle_radius_min = np.array([35.0,  35.0,   35.0]) 
#img_processor0.camera_info.cam[2].circle_radius_max = np.array([150.0, 150.0, 150.0])
#img_processor0.camera_info.cam[2].circle_radius_min = np.array([35.0,  35.0,   35.0])
#img_processor0.camera_info.cam[3].circle_radius_max = np.array([150.0, 150.0, 150.0])
#img_processor0.camera_info.cam[3].circle_radius_min = np.array([35.0,  35.0,   35.0])


img_processor0.camera_info.cam[0].ball_move_rate_img = img_processor0.camera_info.cam[0].circle_radius_max*2            
img_processor0.camera_info.cam[1].ball_move_rate_img = img_processor0.camera_info.cam[1].circle_radius_max*2
img_processor0.camera_info.cam[2].ball_move_rate_img = img_processor0.camera_info.cam[2].circle_radius_max*2
img_processor0.camera_info.cam[3].ball_move_rate_img = img_processor0.camera_info.cam[3].circle_radius_max*2

img_processor0.load_time_str()

t = time.time()

for iteration in range(0,max_frames):
    if iteration == 500:
        a = 1

    if img_processor0.frame_jump_flag == 1:
        for i in range(img_processor0.frame_jump_num):    
            img_processor0.find_next_idx()
    else:
        img_processor0.find_next_idx()

    img_processor0.load_img()
    img_processor0.locate_ball(iteration)

    if img_processor0.frame_jump_flag == 1:
        continue

    with open('cam0_ball_center_2d.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(img_processor0.camera_info.cam[0].img_ball_center[:])

    with open('cam1_ball_center_2d.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(img_processor0.camera_info.cam[1].img_ball_center[:])

    with open('cam2_ball_center_2d.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(img_processor0.camera_info.cam[2].img_ball_center[:])

    with open('cam3_ball_center_2d.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(img_processor0.camera_info.cam[3].img_ball_center[:])

    img_processor0.save_img()
    img_processor0.show_cam_info()
    img_processor0.update_result()


elapsed = time.time() - t
print('\n\n time =',elapsed)    


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

# traj 5
#img_processor0.camera_info.cam[0].circle_radius_max = np.array([64.1668305, 67.17654978, 63.13330659])
#img_processor0.camera_info.cam[0].circle_radius_min = np.array([53.16828489, 56.17800414, 52.13476095])
#img_processor0.camera_info.cam[1].circle_radius_max = np.array([60.39755203, 60.13957149, 51.66194286])
#img_processor0.camera_info.cam[1].circle_radius_min = np.array([49.33489987, 49.07691932, 40.59929069]) 
#img_processor0.camera_info.cam[2].circle_radius_max = np.array([75.66617874, 77.75321059, 72.99556998])
#img_processor0.camera_info.cam[2].circle_radius_min = np.array([66.5627519,  68.64978375, 63.89214313])
#img_processor0.camera_info.cam[3].circle_radius_max = np.array([67.34309341, 64.92429861, 64.18807448])
#img_processor0.camera_info.cam[3].circle_radius_min = np.array([57.21054634, 54.79175154, 54.05127989])

# traj 6
#img_processor0.camera_info.cam[0].circle_radius_max = np.array([64.43563715, 65.34978893, 59.12572924])
#img_processor0.camera_info.cam[0].circle_radius_min = np.array([53.87110048, 54.78525226, 48.56119257])
#img_processor0.camera_info.cam[1].circle_radius_max = np.array([59.40993935, 58.46522304, 53.48542069])
#img_processor0.camera_info.cam[1].circle_radius_min = np.array([48.98643239, 48.04171608, 43.06188336]) 
#img_processor0.camera_info.cam[2].circle_radius_max = np.array([71.39441159, 77.9025526,  77.94702887])
#img_processor0.camera_info.cam[2].circle_radius_min = np.array([61.7330357,  68.2412025,  68.285678])
#img_processor0.camera_info.cam[3].circle_radius_max = np.array([64.50115592, 65.02999397, 63.83800577])
#img_processor0.camera_info.cam[3].circle_radius_min = np.array([54.58483552, 55.11367358, 53.92168538])

# traj 7
#img_processor0.camera_info.cam[0].circle_radius_max = np.array([63.28949717, 65.69660177, 61.08359158])
#img_processor0.camera_info.cam[0].circle_radius_min = np.array([51.8723274,  54.279432,   49.66642181])
#img_processor0.camera_info.cam[1].circle_radius_max = np.array([59.84567117, 59.56068365, 53.04646196])
#img_processor0.camera_info.cam[1].circle_radius_min = np.array([48.02584686, 47.74085934, 41.22663765]) 
#img_processor0.camera_info.cam[2].circle_radius_max = np.array([73.07176994, 76.50223793, 73.68752711])
#img_processor0.camera_info.cam[2].circle_radius_min = np.array([62.66895191, 66.0994199,  63.28470908])
#img_processor0.camera_info.cam[3].circle_radius_max = np.array([67.10694289, 66.02487024, 65.8672883])
#img_processor0.camera_info.cam[3].circle_radius_min = np.array([56.08483032, 55.00275767, 54.84517574])

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

# traj 12
#img_processor0.camera_info.cam[0].circle_radius_max = np.array([70.66003327, 73.24731546, 68.04941754])
#img_processor0.camera_info.cam[0].circle_radius_min = np.array([54.18312831, 56.77041049, 51.57251258])
#img_processor0.camera_info.cam[1].circle_radius_max = np.array([66.95701398, 68.34165563, 94.56428255])
#img_processor0.camera_info.cam[1].circle_radius_min = np.array([49.61921225, 51.0038539,  39.91744253]) 
#img_processor0.camera_info.cam[2].circle_radius_max = np.array([76.10654107, 80.42054216, 83.91475526])
#img_processor0.camera_info.cam[2].circle_radius_min = np.array([58.78089961, 63.09490069, 66.5891138 ])
#img_processor0.camera_info.cam[3].circle_radius_max = np.array([69.76671557, 70.41555266, 70.62012725])
#img_processor0.camera_info.cam[3].circle_radius_min = np.array([54.13866563, 54.78750272, 54.9920773 ])

# traj 13
#img_processor0.camera_info.cam[0].circle_radius_max = np.array([67.73304875, 72.24566054, 62.75119121])
#img_processor0.camera_info.cam[0].circle_radius_min = np.array([55.93283322, 60.44544501, 50.95097568])
#img_processor0.camera_info.cam[1].circle_radius_max = np.array([61.90296786, 62.28985789, 94.59773352])
#img_processor0.camera_info.cam[1].circle_radius_min = np.array([50.50827124, 50.89516127, 39.75535056]) 
#img_processor0.camera_info.cam[2].circle_radius_max = np.array([73.12972602, 81.68635139, 84.00631294])
#img_processor0.camera_info.cam[2].circle_radius_min = np.array([62.13096672, 71.08659219, 73.819085  ])
#img_processor0.camera_info.cam[3].circle_radius_max = np.array([66.29196674, 66.82141447, 69.7970318 ])
#img_processor0.camera_info.cam[3].circle_radius_min = np.array([55.44509272, 55.97454045, 58.95015778])