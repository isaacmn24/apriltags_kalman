#!/usr/bin/env python3

import rospy
import tf2_ros
from geometry_msgs.msg import PoseStamped, QuaternionStamped
from nav_msgs.msg import Odometry
import tf2_geometry_msgs
import numpy as np
import tf.transformations


class TransformListener:
    def __init__(self, publisher_topic, subscriber_topic):
        self.pose = QuaternionStamped()
        self.target_frame = "drone_frame"
        self.source_frame = "world"                 # Initialize to None as withholder
        self.tf_buffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tf_buffer)
        
        rospy.sleep(5)

        self.pub = rospy.Publisher(publisher_topic, PoseStamped, queue_size=10)
        self.sub = rospy.Subscriber(subscriber_topic, PoseStamped, self.read_odom)

        return
    
    def read_odom(self,msg):
        self.pose = msg
        self.source_frame = msg.header.frame_id
        return

    def transform_pose(self):
        """Transforms a pose from the source_frame to the target_frame using TF2."""

        # Create TF buffer and listener

        # Transform pose to target_frame
        transformation = self.tf_buffer.lookup_transform(self.target_frame, self.source_frame,rospy.Time(0))
        transformed_pose = tf2_geometry_msgs.do_transform_pose(self.pose,transformation)
        
        self.pub.publish(transformed_pose)

        print("\033[92m Published transformed pose stamped message\033[0m")
        
        return

if __name__ == '__main__':
    # Initialize ROS node
    rospy.init_node("tf_listener_tag_detection")

    tag_detections_sub_topic = "/anafi/camera/base/attitude"
    tag_detections_pub_topic = "/anafi/camera/transformed_pose"

    transform_listener_tag_detections = TransformListener(tag_detections_pub_topic, tag_detections_sub_topic)

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        # transform_listener_apriltag_odom.transform_pose()
        transform_listener_tag_detections.transform_pose()

        rate.sleep()  # Give some time for TF to populate
