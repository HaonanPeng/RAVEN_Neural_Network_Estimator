#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

def callback(imgmsg):
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(imgmsg, "bgr8")

    cv2.line(img, (640,10), (640,710), (0,255,0) ,1)
    cv2.line(img, (10,360), (1270,360), (0,255,0) ,1)

    cv2.line(img, (340,10), (340,710), (0,255,0) ,1)
    cv2.line(img, (940,10), (940,710), (0,255,0) ,1)

    cv2.line(img, (10,460), (1270,460), (0,255,0) ,1)
    cv2.line(img, (10,560), (1270,560), (0,255,0) ,1)
    cv2.line(img, (10,260), (1270,260), (0,255,0) ,1)
    cv2.line(img, (10,160), (1270,160), (0,255,0) ,1)

    cv2.imshow("Center Line", img)
    cv2.waitKey(4)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/usb_cam0/image_raw", Image, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
