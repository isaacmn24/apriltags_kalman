#!/usr/bin/env python

import rospy
import csv
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, TransformStamped
from std_msgs.msg import Header
from nav_msgs.msg import Odometry
import tf.transformations
import numpy as np
import subprocess
import os

# Bag files
path = "/home/isaac/Downloads/apriltags_kalman/ros_workspace/other_files"
bag_files = [f for f in os.listdir(path) if f.endswith(".bag")]

class DataGenerator():
    def __init__(self):
        self.bag_file = ""
        
        # Define the CSV file
        self.ground_truth_filename = ""
        self.filter_filename       = ""

        self.header = Header()

        return
    
    def initialize(self, test):
        self.bag_file = os.path.join(path, test)
        
        # Define the CSV file
        base_name = os.path.splitext(test)[0]  # Removes .bag
        self.ground_truth_filename = f"ground_truth_data_{base_name}.csv"
        self.filter_filename       = f"filter_data_{base_name}.csv"

        # Write the header for the CSV file
        with open(self.ground_truth_filename, mode="w") as file:
            writer = csv.writer(file)
            writer.writerow(["time_secs", "time_nsecs", "x_ground", "y_ground", "z_ground", "roll_ground", "pitch_ground", "yaw_ground"])

        # Write the header for the CSV file
        with open(self.filter_filename, mode="w") as file:
            writer = csv.writer(file)
            writer.writerow(["time_secs", "time_nsecs", "x_filter", "y_filter", "z_filter", "roll_filter", "pitch_filter", "yaw_filter"])

        self.ground_truth_sub = rospy.Subscriber("/apriltag_box/transformed_odom", Odometry, self.ground_truth_callback)
        self.filter_sub       = rospy.Subscriber("/odometry/filtered", Odometry, self.filter_callback)

        return

    def pose_callback(self, file_name, msg):
        #Callback function for the PoseStamped message.

        # Convert quaternions to euler
        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w

        roll, pitch, yaw = np.degrees(tf.transformations.euler_from_quaternion([qx,qy,qz,qw]))

        # Write to csv
        with open(file_name, mode="a") as file:
            writer = csv.writer(file)
            writer.writerow([
                self.header.stamp.secs,
                self.header.stamp.nsecs,
                msg.pose.pose.position.x,
                msg.pose.pose.position.y,
                msg.pose.pose.position.z,
                roll,pitch, yaw
            ])
            print(f"Logged data to {file_name}")

    def filter_callback(self, msg):
        self.pose_callback(self.filter_filename, msg)

    def ground_truth_callback(self, msg):
        self.header = msg.header
        self.pose_callback(self.ground_truth_filename, msg)

if __name__ == "__main__":
    """Initializes the ROS node and subscriber."""
    rospy.init_node("pose_logger", anonymous=True)

    csv_generator = DataGenerator()

    for test in bag_files:
        bag_file = os.path.join(path, test)

        print("Starting rosbag playback...")
        process = subprocess.Popen(["rosbag", "play", bag_file])

        csv_generator.initialize(test)

        rospy.loginfo("Waiting for rosbag to finish...")
        while process.poll() is None and not rospy.is_shutdown():
            rospy.sleep(0.1)


#    rospy.spin()

