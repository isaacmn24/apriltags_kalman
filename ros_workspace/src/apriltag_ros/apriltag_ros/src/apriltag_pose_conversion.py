#!/usr/bin/env python

import rospy
from apriltag_ros.msg import AprilTagDetectionArray
from geometry_msgs.msg import PoseWithCovarianceStamped

def tag_callback(msg):
    if msg.detections:
        detection = msg.detections[0]  # Take first detection
        pose_msg = PoseWithCovarianceStamped()

        pose_msg = detection.pose
        pose_msg.header.frame_id = "drone_frame"   # EN REALIDAD NO ES DRONE FRAME, ES OPTICAL

        # pose_msg.header = detection.pose.header
        # pose_msg.pose.pose = detection.pose.pose.pose  # Extracting Pose from Odometry
        # pose_msg.pose.covariance = detection.pose.pose.covariance
        
        pose_pub.publish(pose_msg)

if __name__ == '__main__':
    rospy.init_node("tag_converter")
    pose_pub = rospy.Publisher("/apriltag/pose", PoseWithCovarianceStamped, queue_size=10)
    rospy.Subscriber("/tag_detections", AprilTagDetectionArray, tag_callback)
    rospy.spin()
