#!/usr/bin/env python3

import rospy
import tf2_ros
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
import tf2_geometry_msgs
import numpy as np
import tf.transformations

class TransformListener:
    def __init__(self, publisher_topic, subscriber_topic):
        self.pose = PoseStamped()
        self.pose_covariance = np.zeros((6, 6))  # Placeholder for covariance matrix
        # self.target_frame = "hummingbird/real_odometry_sensor"
        # self.source_frame = "hummingbird/camera_link_optical"                 # Initialize to None as withholder
        
        self.target_frame = "anafi_localization_1"
        self.source_frame = "correct_camera_frame" 

        self.tf_buffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tf_buffer)
        
        rospy.sleep(5)

        self.pub = rospy.Publisher(publisher_topic, PoseWithCovarianceStamped, queue_size=10)
        self.sub = rospy.Subscriber(subscriber_topic, PoseWithCovarianceStamped, self.read_odom)

        return
    
    def read_odom(self,msg):
        self.pose.header = msg.header
        self.pose.pose = msg.pose.pose
        self.pose_covariance = np.array(msg.pose.covariance).reshape((6, 6))  # Store as 6x6 matrix
        #self.source_frame = msg.header.frame_id
        return

    def get_transform_matrix(self, target_frame, source_frame, debugging=False):
        try:
            transformation = self.tf_buffer.lookup_transform(target_frame, source_frame, rospy.Time())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            rospy.logwarn(f"Transform lookup failed: {e}")
            return

        # Extract translation and rotation
        trans = transformation.transform.translation
        rot = transformation.transform.rotation

        # Convert quaternion to 4x4 rotation matrix
        quat = [rot.x, rot.y, rot.z, rot.w]
        matrix = tf.transformations.quaternion_matrix(quat)

        # Set translation in the matrix
        matrix[0, 3] = trans.x
        matrix[1, 3] = trans.y
        matrix[2, 3] = trans.z

        if debugging:
            print(f'\nTRANSFORM WITH TARGET: {target_frame} AND SOURCE: {source_frame}\n{transformation}\n\n{matrix}')

        return matrix

    def transform_pose(self):
        # Transform pose to target_frame
        transformation_matrix = self.get_transform_matrix(self.target_frame, self.source_frame)

        transformation = self.tf_buffer.lookup_transform(self.target_frame, self.source_frame, rospy.Time(0))
        transformed_pose = tf2_geometry_msgs.do_transform_pose(self.pose,transformation)
        
        # Extract rotation from transformation
        # q = transformation.transform.rotation
        rotation_matrix = transformation_matrix[:3, :3]
        
        # Apply covariance transformation (R * Cov * R^T)
        transformed_covariance_matrix = np.zeros((6, 6))
        transformed_covariance_matrix[:3, :3] = rotation_matrix @ self.pose_covariance[:3, :3] @ rotation_matrix.T
        transformed_covariance_matrix[3:, 3:] = rotation_matrix @ self.pose_covariance[3:, 3:] @ rotation_matrix.T

        # Convert back to list for ROS message
        transformed_covariance = transformed_covariance_matrix.flatten().tolist()

        transformed_msg = PoseWithCovarianceStamped()
        transformed_msg.header = transformed_pose.header
        transformed_msg.pose.pose = transformed_pose.pose
        transformed_msg.pose.covariance = transformed_covariance
        self.pub.publish(transformed_msg)


        #self.pub.publish(transformed_pose)
        print("\033[92m Published transformed pose stamped message\033[0m")
        
        return

if __name__ == '__main__':
    # Initialize ROS node
    rospy.init_node("tf_listener_tag_detection")

    tag_detections_sub_topic = "/tag_detections_corrected"
    tag_detections_pub_topic = "/tag_detections/transformed_pose"

    transform_listener_tag_detections = TransformListener(tag_detections_pub_topic, tag_detections_sub_topic)

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        # transform_listener_apriltag_odom.transform_pose()
        transform_listener_tag_detections.transform_pose()

        rate.sleep()  # Give some time for TF to populate
