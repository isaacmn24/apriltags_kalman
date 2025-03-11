#!/usr/bin/env python

import rospy
from apriltag_ros.msg import AprilTagDetectionArray
from geometry_msgs.msg import PoseWithCovarianceStamped
import math
import numpy as np

def euclidean_distance(position):
    """Calculate Euclidean distance from the origin."""
    return math.sqrt(position.x**2 + position.y**2 + position.z**2)


def tag_callback(msg):
    if msg.detections:
        # detection = msg.detections[0]  # Take first detection
        distances = []
        for detection in msg.detections:
            position = detection.pose.pose.pose.position  # Extract position from PoseWithCovarianceStamped
            distance = euclidean_distance(position)
            distances.append(distance)
        idx_min = np.argmin(distances)
        

        pose_msg = PoseWithCovarianceStamped()  
        pose_msg = msg.detections[idx_min].pose
        pose_msg.header.frame_id = msg.header.frame_id  # EN REALIDAD NO ES DRONE FRAME, ES OPTICAL

        # pose_msg.header = detection.pose.header
        # pose_msg.pose.pose = detection.pose.pose.pose  # Extracting Pose from Odometry
        # pose_msg.pose.covariance = detection.pose.pose.covariance
        
        pose_pub.publish(pose_msg)

if __name__ == '__main__':
    rospy.init_node("tag_converter")
    pose_pub = rospy.Publisher("/tag_detections_corrected", PoseWithCovarianceStamped, queue_size=10)
    rospy.Subscriber("/tag_detections", AprilTagDetectionArray, tag_callback)
    rospy.spin()
