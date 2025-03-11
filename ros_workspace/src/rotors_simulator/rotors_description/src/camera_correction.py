#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image, CameraInfo

FRAME_ID = "hummingbird/camera_link_optical"  # Make sure this matches the TF frame

def image_callback(msg):
    msg.header.frame_id = FRAME_ID
    img_pub.publish(msg)

def camera_info_callback(msg):
    msg.header.frame_id = FRAME_ID
    cam_info_pub.publish(msg)

if __name__ == '__main__':
    rospy.init_node("camera_frame_id_fixer")
    img_pub = rospy.Publisher("/hummingbird/image_raw_fixed", Image, queue_size=10)
    cam_info_pub = rospy.Publisher("/hummingbird/camera_info_fixed", CameraInfo, queue_size=10)

    rospy.Subscriber("/hummingbird/image_raw", Image, image_callback)
    rospy.Subscriber("/hummingbird/camera_info", CameraInfo, camera_info_callback)

    rospy.spin()
