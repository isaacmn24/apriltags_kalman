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
        # self.source_frame = "apriltag_box/real_odometry_sensor"
        self.source_frame = "world"
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
    
    def apply_transform(self, transform, pose, debugging=False):
        pos = pose.pose.position
        ori = pose.pose.orientation

        new_pose = np.array([
            pos.x + transform[0,3],
            pos.y + transform[1,3],
            pos.z + transform[2,3]
            ])

        # Convert quaternion to rotation matrix
        quat = [ori.x, ori.y, ori.z, ori.w]
        matrix = tf.transformations.quaternion_matrix(quat)  # 4x4 rotation matrix

        new_ori = np.dot(transform[0:3, 0:3], matrix[0:3, 0:3])
        new_ori_extended = np.identity(4)
        new_ori_extended[:3, :3] = new_ori

        pose_matrix = matrix
        pose_matrix[0,3] = pos.x
        pose_matrix[1,3] = pos.y
        pose_matrix[2,3] = pos.z

        new_ori_extended = np.dot(transform, pose_matrix)


        new_ori = tf.transformations.quaternion_from_matrix(new_ori_extended)

        transformed_pose = PoseStamped()
        transformed_pose.header = pose.header
        transformed_pose.pose.position.x = new_ori_extended[0,3]
        transformed_pose.pose.position.y = new_ori_extended[1,3]
        transformed_pose.pose.position.z = new_ori_extended[2,3]

        transformed_pose.pose.orientation.x = new_ori[0]
        transformed_pose.pose.orientation.y = new_ori[1]
        transformed_pose.pose.orientation.z = new_ori[2]
        transformed_pose.pose.orientation.w = new_ori[3]

        

        if debugging:
            print(f'\nTRANSFORM:\n{transform}\n\nOLD POSE:\n{matrix}\n\nNEW POSE:\n{new_pose}\n\nNEW ORIENTATION:\n{new_ori}\n\nTRANSFORMED POSE:\n{transformed_pose}')

        return transformed_pose

    def transform_odom(self):
        # Transform pose to target_frame
        # transformation = self.tf_buffer.lookup_transform(self.target_frame, self.source_frame,rospy.Time(0))

        transformation_matrix = self.get_transform_matrix(self.target_frame, self.source_frame)

        """ POSE TRANSFORMATION """
        # transformed_pose = tf2_geometry_msgs.do_transform_pose(self.pose,transformation)
        transformed_pose = self.apply_transform(transformation_matrix, self.pose)
        
        # Extract rotation from transformation
        # q = transformation.transform.rotation
        rotation_matrix = transformation_matrix[:3, :3]  # Extract 3x3 rotation
        
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
        transformed_msg.header.frame_id = self.target_frame
        transformed_msg.child_frame_id = "apriltag_box/real_odometry_sensor"
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
