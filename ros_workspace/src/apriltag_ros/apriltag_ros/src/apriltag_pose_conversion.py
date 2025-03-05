#!/usr/bin/env python

import rospy
from apriltag_ros.msg import AprilTagDetectionArray
from geometry_msgs.msg import PoseStamped

def tag_callback(msg):
    if msg.detections:
        detection = msg.detections[0]  # Take first detection
        pose_msg = PoseStamped()
        pose_msg.header = detection.pose.header
        pose_msg.pose = detection.pose.pose.pose  # Extracting Pose from Odometry
        pose_pub.publish(pose_msg)

if __name__ == '__main__':
    rospy.init_node("tag_converter")
    pose_pub = rospy.Publisher("/apriltag/pose", PoseStamped, queue_size=10)
    rospy.Subscriber("/tag_detections", AprilTagDetectionArray, tag_callback)
    rospy.spin()
