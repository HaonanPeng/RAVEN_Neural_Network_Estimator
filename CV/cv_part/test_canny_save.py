
import os
import cv2
import numpy as np


def load_images_from_folder(folder): 
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        print(filename)
        if img is not None:
            images.append(img)            
    return images

print('File names:\n')
folder = r'D:\iCloudDrive\Research Credit\Test - Full - March 6\canny_test'
images = load_images_from_folder(folder)

for i in range (len(images)):
    img = images[i]
    h, w = img.shape[:2]

    red = np.float32(img[:,:,2])
    green = np.float32(img[:,:,1])
    blue = np.float32(img[:,:,0])  

    red_new = (np.square(red/60)*100).clip(min=0,max=255)
    green_new = (np.square(red/60)*100).clip(min=0,max=255)
    blue_new = (np.square(red/60)*100).clip(min=0,max=255)          

    new_img = np.zeros((h,w,3))
    new_img[:,:,0] = blue_new
    new_img[:,:,1] = green_new
    new_img[:,:,2] = red_new
    new_img = np.uint8(new_img)

    cv2.imshow("show",new_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

    img = cv2.GaussianBlur(img, (0,0), 4)
    gray = cv2.Canny(img,10,50)
    name = str(i)+'.jpg'
    cv2.imwrite(name,gray)