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
        folder_name = '/home/haonan/catkin_ws/src/raven_img_recorder/src/bagfiles/'

        topic_name = "ravenstate"
        bag_name = folder_name + 'raven_state_recorder.bag'
        txt_folder_name = folder_name


        first_call = 0
        txt_name = txt_folder_name + "raven_state.txt"
        with rosbag.Bag(bag_name , 'r') as bag:
            for topic,msg,t in bag.read_messages():

                timestr = "%.6f" %  msg.hdr.stamp.to_sec()

                if first_call ==0:
                    txt_writer = open(txt_name, 'w')

                    txt_writer.write(timestr)
                    txt_writer.write(" ")

                    for index in range(0,6):
                        txt_writer.write("%.6f" % msg.pos_d[index])
                        txt_writer.write(" ")

                    for index in range(0,18):
                        txt_writer.write("%.6f" % msg.ori[index])
                        txt_writer.write(" ")

                    for index in range(0,18):
                        txt_writer.write("%.6f" % msg.ori_d[index])
                        txt_writer.write(" ")

                    for index in range(0,16):
                        txt_writer.write("%.6f" % msg.encVals[index])
                        txt_writer.write(" ")

                    for index in range(0,16):
                        txt_writer.write("%.6f" % msg.dac_val[index])
                        txt_writer.write(" ")

                    for index in range(0,16):
                        txt_writer.write("%.6f" % msg.tau[index])
                        txt_writer.write(" ")

                    for index in range(0,16):
                        txt_writer.write("%.6f" % msg.mpos[index])
                        txt_writer.write(" ")

                    for index in range(0,16):
                        txt_writer.write("%.6f" % msg.jpos[index])
                        txt_writer.write(" ")

                    for index in range(0,16):
                        txt_writer.write("%.6f" % msg.mvel[index])
                        txt_writer.write(" ")

                    for index in range(0,16):
                        txt_writer.write("%.6f" % msg.jvel[index])
                        txt_writer.write(" ")

                    for index in range(0,16):
                        txt_writer.write("%.6f" % msg.mpos_d[index])
                        txt_writer.write(" ")

                    for index in range(0,16):
                        txt_writer.write("%.6f" % msg.jpos_d[index])
                        txt_writer.write(" ")

                    for index in range(0,2):
                        txt_writer.write("%.6f" % msg.grasp_d[index])
                        txt_writer.write(" ")

                    for index in range(0,16):
                        txt_writer.write("%.6f" % msg.encoffsets[index])
                        txt_writer.write(" ")

                    for index in range(0,12):
                        txt_writer.write("%.6f" % msg.jac_vel[index])
                        txt_writer.write(" ")

                    for index in range(0,12):
                        txt_writer.write("%.6f" % msg.jac_f[index])
                        txt_writer.write(" ")

                    for index in range(0,6):
                        txt_writer.write("%.6f" % msg.pos[index])
                        txt_writer.write(" ")

                    txt_writer.write('\n')

                    txt_writer.close()
                    first_call = 1
                    txt_writer = open(txt_name, 'a')


                else:

                    txt_writer.write(timestr)
                    txt_writer.write(" ")

                    for index in range(0, 6):
                        txt_writer.write("%.6f" % msg.pos_d[index])
                        txt_writer.write(" ")

                    for index in range(0, 18):
                        txt_writer.write("%.6f" % msg.ori[index])
                        txt_writer.write(" ")

                    for index in range(0, 18):
                        txt_writer.write("%.6f" % msg.ori_d[index])
                        txt_writer.write(" ")

                    for index in range(0, 16):
                        txt_writer.write("%.6f" % msg.encVals[index])
                        txt_writer.write(" ")

                    for index in range(0, 16):
                        txt_writer.write("%.6f" % msg.dac_val[index])
                        txt_writer.write(" ")

                    for index in range(0, 16):
                        txt_writer.write("%.6f" % msg.tau[index])
                        txt_writer.write(" ")

                    for index in range(0, 16):
                        txt_writer.write("%.6f" % msg.mpos[index])
                        txt_writer.write(" ")

                    for index in range(0, 16):
                        txt_writer.write("%.6f" % msg.jpos[index])
                        txt_writer.write(" ")

                    for index in range(0, 16):
                        txt_writer.write("%.6f" % msg.mvel[index])
                        txt_writer.write(" ")

                    for index in range(0, 16):
                        txt_writer.write("%.6f" % msg.jvel[index])
                        txt_writer.write(" ")

                    for index in range(0, 16):
                        txt_writer.write("%.6f" % msg.mpos_d[index])
                        txt_writer.write(" ")

                    for index in range(0, 16):
                        txt_writer.write("%.6f" % msg.jpos_d[index])
                        txt_writer.write(" ")

                    for index in range(0, 2):
                        txt_writer.write("%.6f" % msg.grasp_d[index])
                        txt_writer.write(" ")

                    for index in range(0, 16):
                        txt_writer.write("%.6f" % msg.encoffsets[index])
                        txt_writer.write(" ")

                    for index in range(0, 12):
                        txt_writer.write("%.6f" % msg.jac_vel[index])
                        txt_writer.write(" ")

                    for index in range(0, 12):
                        txt_writer.write("%.6f" % msg.jac_f[index])
                        txt_writer.write(" ")

                    for index in range(0,6):
                        txt_writer.write("%.6f" % msg.pos[index])
                        txt_writer.write(" ")


                    txt_writer.write('\n')

if __name__ == '__main__':

    #rospy.init_node(PKG)

    try:
        image_creator = ImageCreator()
        rospy.loginfo("[RAVEN_IMG_RECORDER]: Raven state read complete, Camera: ")
    except rospy.ROSInterruptException:
        pass
