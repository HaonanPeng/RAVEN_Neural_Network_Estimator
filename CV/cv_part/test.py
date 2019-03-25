import os
import cv2
import numpy as np

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

red = np.asarray(img[:,:,2])
green = np.asarray(img[:,:,1])
blue = np.asarray(img[:,:,0])

ones = np.ones((h,w))
gray = ones-np.multiply((ones-red/255),(ones-green/255))

print(gray[500:510,600:610])
gray = np.uint8(gray)
#cv2.imshow("show",gray)
cv2.imshow("show",gray)
print(gray[500:510,600:610])

cv2.waitKey(0)
cv2.destroyAllWindows() 