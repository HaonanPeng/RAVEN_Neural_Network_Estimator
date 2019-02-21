import cv2
import math
import numpy as np
import func_circle_detect as f_cd
import os


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        print(filename)
        if img is not None:
            images.append(img)            
    return images

print('File names:\n')
folder = r'D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 11\Camera Calibration\Ground Truth - Balls\2'
images = load_images_from_folder(folder)

print('\nGround Truth Balls - Set 0---------\n')
#Image_object_center, Image_object_radius, img_result = f_cd.circle_center_detect (images[1], 1)
#Image_object_center, img_result = f_cd.circle_center_detect (images[3], 1)

for i in range(3):
    Image_object_center, Image_object_radius, img_result = f_cd.circle_center_detect (images[i], 1,30,60)
    print('cam_%d Center_2D:\n' % i)
    print('%.1f %.1f\n%.1f %.1f\n%.1f %.1f\n\n' % (Image_object_center[0:1,0:1], Image_object_center[0:1,1:2],Image_object_center[1:2,0:1], Image_object_center[1:2,1:2],Image_object_center[2:3,0:1], Image_object_center[2:3,1:2],))
    print('%.1f %.1f %.1f \n' % (Image_object_radius[0],Image_object_radius[1],Image_object_radius[2],))

       