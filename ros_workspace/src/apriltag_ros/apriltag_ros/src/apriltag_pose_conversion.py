#!/usr/bin/env python

import rospy
from apriltag_ros.msg import AprilTagDetectionArray
from geometry_msgs.msg import PoseWithCovarianceStamped, Pose
import math
import numpy as np
import pickle
import tf.transformations

# These sizes are from covariance_mapping.py
bin_sizes = [0.3, 0.3, 0.3, 15, 15, 15]     # x,y,z,roll,pitch,yaw

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
        pose_msg.header.frame_id = 'hummingbird/camera_link_optical' 
        
        measured_position = [pose_msg.pose.pose.position.x,
                             pose_msg.pose.pose.position.y,
                             pose_msg.pose.pose.position.z]

        orientation = pose_msg.pose.pose.orientation
        quaternion = [orientation.x, orientation.y, orientation.z, orientation.w]
        roll, pitch, yaw = tf.transformations.euler_from_quaternion(quaternion)
        roll = np.degrees(roll)
        pitch = np.degrees(pitch)
        yaw = np.degrees(yaw)

        # print(f'Angles: roll = {roll}, pitch = {pitch}, yaw = {yaw}')
        # measured_position.extend([roll, pitch, yaw])
        # print(measured_position)

        # Here we get the multiple of the measured data with respect to the bin sizes
        for coordinate in range(len(measured_position)):
            measured_position[coordinate] = np.round(measured_position[coordinate] / bin_sizes[coordinate]) * bin_sizes[coordinate]

        measured_position = tuple(np.round(measured_position,1))
        # print(measured_position)

        cov_matrix = get_covariance(measured_position)
        #cov_matrix = [0.0765746754287511, 0.008739799427283122, 0.026557858049306413, -0.36865153842901704, 0.017567690855414708, -0.9404853931948389, 0.008739799427283122, 0.0022796865259336234, 0.0017037886292318573, -0.01908984277462361, -0.006026910316131032, -0.1579827380639132, 0.026557858049306413, 0.0017037886292318573, 0.011327571756667001, -0.1810711313460202, -0.005148429956196565, -0.27570977336058367, -0.36865153842901704, -0.01908984277462361, -0.1810711313460202, 3.432362696175498, 0.8453014018460459, 3.7724643758448733, 0.017567690855414708, -0.006026910316131032, -0.005148429956196565, 0.8453014018460459, 1.7927427284266244, 0.3687691933562567, -0.9404853931948389, -0.1579827380639132, -0.27570977336058367, 3.7724643758448733, 0.3687691933562567, 13.667208890049714]

        pose_msg.pose.covariance = cov_matrix
        pose_pub.publish(pose_msg)

def get_covariance(measured_position):
    cov_matrix = covariance_matrices.get(measured_position, np.eye(6) * 1e-3)  # Default: small identity matrix
    
    # We flatten the matrix to 1D for that's what ROS accepts
    cov_matrix = [item for sublist in cov_matrix for item in sublist]

    print(f'Bin: {measured_position} : {cov_matrix}')

    return cov_matrix

if __name__ == '__main__':
    rospy.init_node("tag_converter")

    with open("/home/raven/src/apriltags_kalman/ros_workspace/covariance_matrices.pkl", "rb") as f:
        covariance_matrices = pickle.load(f)
        print(covariance_matrices.keys())

    pose_pub = rospy.Publisher("/tag_detections_corrected", PoseWithCovarianceStamped, queue_size=10)
    rospy.Subscriber("/tag_detections", AprilTagDetectionArray, tag_callback)
    rospy.spin()
