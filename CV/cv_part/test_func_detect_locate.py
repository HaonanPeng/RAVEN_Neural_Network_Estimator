import func_camera_info_process as f_cip
import os
import cv2
import func_circle_detect as f_cd

camera_info = f_cip.camera_info()

def load_images_from_folder(folder): 
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        print(filename)
        if img is not None:
            images.append(img)            
    return images

print('File names:\n')
folder = r'C:\Users\Xingjian Yang\iCloudDrive\Research Credit\Test - Full - March 6\img_test_sample'
images = load_images_from_folder(folder)


camera_info = f_cip.camera_info()
ball_center, img_result_list, eff_cam_num = camera_info.detect_locate(images)
print(ball_center) 