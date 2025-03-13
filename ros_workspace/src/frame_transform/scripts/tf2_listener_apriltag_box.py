#!/usr/bin/env python3

import rospy
import tf2_ros
from geometry_msgs.msg import PoseStamped, TwistStamped
from nav_msgs.msg import Odometry
import tf2_geometry_msgs
import numpy as np
import tf.transformations


class TransformListener:
    def __init__(self, publisher_topic, subscriber_topic):
        self.pose = PoseStamped()
        self.pose_covariance = np.zeros((6, 6))  # Placeholder for covariance matrix
        self.twist = TwistStamped()
        self.twist_covariance = np.zeros((6, 6))
        self.target_frame = "hummingbird/real_odometry_sensor"
        self.source_frame = "apriltag_box/real_odometry_sensor"                 # Initialize to None as withholder
        self.tf_buffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tf_buffer)
        
        rospy.sleep(5)

        self.pub = rospy.Publisher(publisher_topic, Odometry, queue_size=10)
        self.sub = rospy.Subscriber(subscriber_topic, Odometry, self.read_odom)

        return
    
    def read_odom(self,msg):
        self.pose.header = msg.header
        self.pose.pose = msg.pose.pose
        self.pose_covariance = np.array(msg.pose.covariance).reshape((6, 6))  # Store as 6x6 matrix

        self.twist.header = msg.header
        self.twist.twist = msg.twist.twist
        self.twist_covariance = np.array(msg.twist.covariance).reshape((6, 6))

        self.source_frame = msg.header.frame_id
        return

    def transform_odom(self):
        """Transforms a pose from the source_frame to the target_frame using TF2."""

        # Create TF buffer and listener
        
        # # If message wasn't received before calling current function
        # if self.source_frame is None:
        #     return

        # Transform pose to target_frame
        transformation = self.tf_buffer.lookup_transform(self.target_frame, self.source_frame,rospy.Time(0))

        """ POSE TRANSFORMATION """
        transformed_pose = tf2_geometry_msgs.do_transform_pose(self.pose,transformation)
        
        # Extract rotation from transformation
        q = transformation.transform.rotation
        rotation_matrix = tf.transformations.quaternion_matrix([q.x, q.y, q.z, q.w])[:3, :3]  # Extract 3x3 rotation
        
        # Apply covariance transformation (R * Cov * R^T)
        transformed_pose_covariance_matrix = np.zeros((6, 6))
        transformed_pose_covariance_matrix[:3, :3] = rotation_matrix @ self.pose_covariance[:3, :3] @ rotation_matrix.T
        transformed_pose_covariance_matrix[3:, 3:] = rotation_matrix @ self.pose_covariance[3:, 3:] @ rotation_matrix.T

        # Convert back to list for ROS message
        transformed_pose_covariance = transformed_pose_covariance_matrix.flatten().tolist()

        """ TWIST TRANSFORMATION """
        transformed_twist = TwistStamped()
        transformed_twist.header = self.twist.header
        transformed_twist.twist.linear.x, transformed_twist.twist.linear.y, transformed_twist.twist.linear.z = \
            rotation_matrix @ np.array([
                self.twist.twist.linear.x,
                self.twist.twist.linear.y,
                self.twist.twist.linear.z
            ])

        transformed_twist.twist.angular.x, transformed_twist.twist.angular.y, transformed_twist.twist.angular.z = \
            rotation_matrix @ np.array([
                self.twist.twist.angular.x,
                self.twist.twist.angular.y,
                self.twist.twist.angular.z
            ])

        # Apply twist covariance transformation (R * Cov * R^T)
        transformed_twist_covariance_matrix = np.zeros((6, 6))
        transformed_twist_covariance_matrix[:3, :3] = rotation_matrix @ self.twist_covariance[:3, :3] @ rotation_matrix.T
        transformed_twist_covariance_matrix[3:, 3:] = rotation_matrix @ self.twist_covariance[3:, 3:] @ rotation_matrix.T

        transformed_twist_covariance = transformed_twist_covariance_matrix.flatten().tolist()

        """ PUBLISH TRANSFORMED ODOMETRY """

        transformed_msg = Odometry()
        transformed_msg.header = transformed_pose.header
        transformed_msg.child_frame_id = self.source_frame
        transformed_msg.pose.pose = transformed_pose.pose
        transformed_msg.pose.covariance = transformed_pose_covariance
        transformed_msg.twist.twist = transformed_twist.twist
        transformed_msg.twist.covariance = transformed_twist_covariance

        self.pub.publish(transformed_msg)

        #self.pub.publish(transformed_pose)
        print("\033[92m Published transformed pose stamped message\033[0m")
        
        return

if __name__ == '__main__':
    # Initialize ROS node
    rospy.init_node("tf_listener_apriltag_box")

    apriltag_odom_sub_topic = "/apriltag_box/real_odometry_sensor/odometry"
    apriltag_odom_pub_topic = "/apriltag_box/transformed_odom"

    transform_listener_apriltag_odom = TransformListener(apriltag_odom_pub_topic, apriltag_odom_sub_topic)

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        transform_listener_apriltag_odom.transform_odom()
        # transform_listener_tag_detections.transform_pose()

        rate.sleep()  # Give some time for TF to populate
