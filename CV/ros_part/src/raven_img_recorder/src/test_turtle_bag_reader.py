#!/usr/bin/env python

# Extract images from a bag file.

#PKG = 'beginner_tutorials'
import roslib   #roslib.load_manifest(PKG)
import rosbag
import rospy
import sys
import numpy as np
from geometry_msgs.msg import Twist
# Reading bag filename from command line or roslaunch parameter.
#import os
#import sys


class ImageCreator():


    def __init__(self):
        topic_name = "/usb_cam0/image_raw"
        bag_name = '/home/haonan/catkin_ws/src/raven_img_recorder/src/bagfiles/turtlesim_recorder.bag'
        txt_folder_name = "/home/haonan/catkin_ws/src/raven_img_recorder/src/bagfiles/"


        first_call = 0
        txt_name = txt_folder_name + "turtle_sim_state.txt"
        with rosbag.Bag(bag_name , 'r') as bag:
            for topic,msg,t in bag.read_messages():
                #timestr = "%.6f" %  msg.header.stamp.to_sec()
                x = "%.6f" % msg.linear.x
                y = "%.6f" %  msg.linear.y
                z = "%.6f" % msg.linear.z

                print(x)
                print("______________________________________________________________")
                if first_call ==0:
                    txt_writer = open(txt_name, 'w')

                    txt_writer.write(x)
                    txt_writer.write(' ')

                    txt_writer.write(y)
                    txt_writer.write(' ')

                    txt_writer.write(z)
                    txt_writer.write('\n')

                    txt_writer.close()
                    first_call = 1
                    txt_writer = open(txt_name, 'a')
                else:

                    txt_writer.write(x)
                    txt_writer.write(' ')

                    txt_writer.write(y)
                    txt_writer.write(' ')

                    txt_writer.write(z)
                    txt_writer.write('\n')

if __name__ == '__main__':

    #rospy.init_node(PKG)

    try:
        image_creator = ImageCreator()
    except rospy.ROSInterruptException:
        pass
