import os
import cv2
import numpy as np
import time


def load_imgs_from_folder(folder): 
    imgs = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        print(filename)
        if img is not None:
            imgs.append(img)            
    return imgs

folder = r'C:\Users\Xingjian Yang\iCloudDrive\Research Credit\Test - Full - March 6\img_test_sample'
imgs = load_imgs_from_folder(folder)



img = imgs[0]
h, w = img.shape[:2]

########################
red = np.float32(img[:,:,2])
green = np.float32(img[:,:,1])
blue = np.float32(img[:,:,0])   

channel_ball_2 = np.uint8((red-green).clip(min=0)) # red
channel_ball_0 = np.uint8((green-red).clip(min=0)) # green
channel_ball_1 = np.uint8((((red-blue).clip(min=0)-3*channel_ball_2)*2).clip(min=0))  # yellow

#(T, ball_0_thresh) = cv2.threshold(ball_1, 30, 255, cv2.THRESH_BINARY)#阈值化处理，阈值为：155

#cv2.imshow("show",channel_ball_1)    
#cv2.waitKey(0)
#cv2.destroyAllWindows() 


#########################
ref_color = np.array([[220,250,130],[180,250,170],[250,80,190]])

num_ball = 3
channel = np.zeros((h,w,num_ball))

for idx_ball in range(num_ball):
    
    d_r = np.absolute(np.ones((h,w))*ref_color[idx_ball,0]-img[:,:,0])
    d_g = np.absolute(np.ones((h,w))*ref_color[idx_ball,1]-img[:,:,1])
    d_b = np.absolute(np.ones((h,w))*ref_color[idx_ball,2]-img[:,:,2])

    d_r = np.square(d_r)
    d_g = np.square(d_g)
    d_b = np.square(d_b)
    channel[:,:,idx_ball] = (np.ones((h,w))*255-(d_r+d_g+d_b)/60).clip(min=0)


#cv2.imshow("show",np.uint8(channel[:,:,1]))    
#cv2.waitKey(0)
#cv2.destroyAllWindows() 

channel_new = np.zeros((h,w,num_ball))
for idx_ball in range(num_ball):
    list_remain = list(range(num_ball))
    list_remain.remove(idx_ball)
    
    print(list_remain)
    
    channel_remain_avg = np.zeros((h,w))
    for i in range(len(list_remain)):
        idx_ball_2 = list_remain[i]
        channel_remain_avg += channel[:,:,idx_ball_2]
    channel_remain_avg = channel_remain_avg/len(list_remain)

    channel_new[:,:,idx_ball] = np.uint8((channel[:,:,idx_ball]-channel_remain_avg).clip(min=0))

cv2.imshow("show",channel_new[:,:,2])    
cv2.waitKey(0)
cv2.destroyAllWindows() 


