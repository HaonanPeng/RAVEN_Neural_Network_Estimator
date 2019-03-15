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

red = np.float32(img[:,:,2])
green = np.float32(img[:,:,1])
blue = np.float32(img[:,:,0])

ones = np.ones((h,w))
gray = ones-np.multiply((ones-red/255),(ones-green/255))


a = np.array([1,2,3,4,5,6,7,8,9])
print(a.clip(3,6))

t = time.time()
ball_1 = np.uint8((red-green).clip(min=0))
ball_1 = np.uint8((green-red).clip(min=0))
ball_2 = np.uint8(((red-blue).clip(min=0)-ball_0).clip(min=0))
elapsed = time.time() - t
print('\n\n time =',elapsed)    

cv2.imshow("show",ball_0)    
cv2.waitKey(0)
cv2.destroyAllWindows() 
