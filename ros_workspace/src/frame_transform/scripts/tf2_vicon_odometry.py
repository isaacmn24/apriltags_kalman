#!/usr/bin/env python3

import rospy
import tf2_ros
from geometry_msgs.msg import PoseStamped, TwistStamped
from nav_msgs.msg import Odometry
import tf2_geometry_msgs
import numpy as np
import tf.transformations

class Odom():
    def __init__(self):
        self.pose = PoseStamped()
        self.twist = TwistStamped()

        rospy.Subscriber("/vrpn_client_node/marker_board_1/pose", PoseStamped, self.read_pose)
        rospy.Subscriber("/vrpn_client_node/marker_board_1/twist", TwistStamped, self.read_twist)
        
        self.pub = rospy.Publisher("/apriltag_box/transformed_odom", Odometry, queue_size=10)

        return
    
    def read_pose(self, msg):
        self.pose = msg
        return
    
    def read_twist(self, msg):
        self.twist = msg
        return
    
    def publish_odometry(self):
        covariance = np.array(36*[0])   # Assuming vicon is ground truth its covariance is 0

        transformed_msg = Odometry()
        transformed_msg.header = self.pose.header
        transformed_msg.child_frame_id = "marker_board_1"
        transformed_msg.pose.pose = self.pose.pose
        transformed_msg.pose.covariance = covariance
        transformed_msg.twist.twist = self.twist.twist
        transformed_msg.twist.covariance = covariance

        self.pub.publish(transformed_msg)

        print("Odometry published")

        return

if __name__ == '__main__':
    # Initialize ROS node
    rospy.init_node("vicon_odometry")

    odom = Odom()

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        odom.publish_odometry()
        rate.sleep()  # Give some time for TF to populate
