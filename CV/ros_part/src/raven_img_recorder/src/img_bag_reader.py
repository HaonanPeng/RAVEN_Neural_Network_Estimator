#!/usr/bin/env python

# Extract images from a bag file.

#PKG = 'beginner_tutorials'
import roslib   #roslib.load_manifest(PKG)
import rosbag
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from cv_bridge import CvBridgeError
import sys

# Reading bag filename from command line or roslaunch parameter.
#import os
#import sys


class ImageCreator():


    def __init__(self,camera_num):

        folder_name = '/home/haonan/catkin_ws/src/raven_img_recorder/src/bagfiles/'

        print("Chosen Camera:")
        print(camera_num)
        if camera_num == "camera0" :
            topic_name = "/usb_cam0/image_raw"
            bag_name = folder_name + 'camera0_recorder.bag'
            img_folder_name = folder_name + "img_camera0/"
        elif camera_num == "camera1" :
            topic_name = "/usb_cam1/image_raw"
            bag_name = folder_name + 'camera1_recorder.bag'
            img_folder_name = folder_name + "img_camera1/"
        elif camera_num == "camera2" :
            topic_name = "/usb_cam2/image_raw"
            bag_name = folder_name + 'camera2_recorder.bag'
            img_folder_name = folder_name + "img_camera2/"
        elif camera_num == "camera3" :
            topic_name = "/usb_cam3/image_raw"
            bag_name = folder_name + 'camera3_recorder.bag'
            img_folder_name = folder_name + "img_camera3/"
        else:
            sys.exit("Unknown camera. Available choice should be: camera0, camera1, camera2, camera3")


        self.bridge = CvBridge()


        first_call = 0
        txt_name = img_folder_name + "time_stemp_" + camera_num + ".txt"
        with rosbag.Bag(bag_name , 'r') as bag:
            for topic,msg,t in bag.read_messages():
                if topic == topic_name:
                        try:
                            cv_image = self.bridge.imgmsg_to_cv2(msg,"bgr8")
                        except CvBridgeError as e:
                            print e
                        timestr = "%.6f" %  msg.header.stamp.to_sec()

                        image_name = img_folder_name + timestr + ".jpg"
                        #image_name = timestr + ".jpg"
                        #cv2.imshow("img", cv_image)
                        #cv2.waitKey(30)

                        cv2.imwrite(image_name, cv_image)
                        if first_call ==0:
                            txt_writer = open(txt_name, 'w')
                            txt_writer.write(timestr)
                            txt_writer.write(' ')
                            txt_writer.close()
                            first_call = 1
                            txt_writer = open(txt_name, 'a')
                        else:
                            txt_writer.write(timestr)
                            txt_writer.write(' ')

if __name__ == '__main__':

    #rospy.init_node(PKG)

    try:
        #camera_num = "camera0"
        camera_num = sys.argv[1]
        image_creator = ImageCreator(camera_num)
    except rospy.ROSInterruptException:
        pass
