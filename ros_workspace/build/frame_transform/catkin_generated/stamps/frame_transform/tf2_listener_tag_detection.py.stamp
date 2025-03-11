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
        self.target_frame = "drone_frame"
        self.source_frame = None                 # Initialize to None as withholder
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
        self.source_frame = msg.header.frame_id
        return

    def transform_pose(self):
        """Transforms a pose from the source_frame to the target_frame using TF2."""

        # Create TF buffer and listener
        
        # If message wasn't received before calling current function
        if self.source_frame is None:
            return

        # Transform pose to target_frame
        transformation = self.tf_buffer.lookup_transform(self.target_frame, self.source_frame,rospy.Time(0))
        transformed_pose = tf2_geometry_msgs.do_transform_pose(self.pose,transformation)
        
        # Extract rotation from transformation
        q = transformation.transform.rotation
        rotation_matrix = tf.transformations.quaternion_matrix([q.x, q.y, q.z, q.w])[:3, :3]  # Extract 3x3 rotation
        
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

    # apriltag_odom_sub_topic = "/apriltag_box/real_odometry_sensor/pose_with_covariance"
    # apriltag_odom_pub_topic = "/apriltag_box/transformed_pose"

    tag_detections_sub_topic = "/tag_detections"
    tag_detections_pub_topic = "/tag_detections/transformed_pose"

    #transform_listener_tag_detections = TransformListener(tag_detections_pub_topic, tag_detections_sub_topic)
    # transform_listener_apriltag_odom = TransformListener(apriltag_odom_pub_topic, apriltag_odom_sub_topic)
    transform_listener_tag_detections = TransformListener(tag_detections_pub_topic, tag_detections_sub_topic)

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        # transform_listener_apriltag_odom.transform_pose()
        transform_listener_tag_detections.transform_pose()

        rate.sleep()  # Give some time for TF to populate
