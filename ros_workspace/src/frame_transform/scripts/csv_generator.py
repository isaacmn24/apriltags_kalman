#!/usr/bin/env python

import rospy
import csv
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, TransformStamped, Pose
from std_msgs.msg import Header
from nav_msgs.msg import Odometry
import tf.transformations as tft
import numpy as np
import subprocess
import os

root = "/home/isaac/Desktop/other_files/outside_tests/"

# Bag files
path = f"{root}bag files"
bag_files = [f for f in os.listdir(path) if f.endswith(".bag")]

print(bag_files)

#bag_files = ['bottom_right.bag', 'center_center.bag', 'bottom_left.bag', 'bottom_center.bag', 'top_center.bag', 'center_right.bag', 'top_right.bag', 'top_left.bag', 'center_left.bag']

csv_path = f"{root}csv files"

class DataGenerator():
    def __init__(self):
        self.bag_file = ""
        
        # Define the CSV file
        self.ground_truth_filename = ""
        self.filter_filename       = ""
        self.error_filename        = ""

        self.header = Header()

        self.ground_truth_pose = Pose()
        self.filter_pose       = Pose()

        return
    
    def initialize(self, test):
        self.bag_file = os.path.join(path, test)
        
        # Define the CSV file
        base_name = os.path.splitext(test)[0]  # Removes .bag
        self.ground_truth_filename = f"{csv_path}/ground_truth_data_{base_name}.csv"
        self.filter_filename       = f"{csv_path}/filter_data_{base_name}.csv"
        self.error_filename        = f"{csv_path}/error_data_{base_name}.csv"

        with open(self.ground_truth_filename, mode="w") as file:
            writer = csv.writer(file)
            writer.writerow(["time_secs", "time_nsecs", "x", "y", "z", "roll", "pitch", "yaw"])

        # Write the header for the CSV file
        with open(self.filter_filename, mode="w") as file:
            writer = csv.writer(file)
            writer.writerow(["time_secs", "time_nsecs", "x", "y", "z", "roll", "pitch", "yaw"])

        with open(self.error_filename, mode="w") as file:
            writer = csv.writer(file)
            writer.writerow(["time_secs", "time_nsecs", "x", "y", "z", "roll", "pitch", "yaw"])

        self.ground_truth_sub = rospy.Subscriber("/apriltag_box/transformed_odom", Odometry, self.ground_truth_callback)
        self.filter_sub       = rospy.Subscriber("/odometry/filtered", Odometry, self.filter_callback)

        return
    
    def calculate_error(self):
        q = self.filter_pose.orientation
        quaternions_filter = [q.x, q.y, q.z, q.w]
        q_inv = tft.quaternion_inverse(quaternions_filter)

        q = self.ground_truth_pose
        quaternions_ground_truth = [q.x, q.y, q.z, q.w]

        q_error = tft.quaternion_multiply(quaternions_ground_truth, q_inv)

        roll, pitch, yaw = np.degrees(tft.euler_from_quaternion(q_error))

        dx = self.ground_truth_pose.position.x - self.filter_pose.position.x
        dy = self.ground_truth_pose.position.y - self.filter_pose.position.y
        dz = self.ground_truth_pose.position.z - self.filter_pose.position.z

        print(dx,dy,dz,roll,pitch,yaw)

        # Write to csv
        with open(self.error_filename, mode="a") as file:
            writer = csv.writer(file)
            writer.writerow([
                self.header.stamp.secs,
                self.header.stamp.nsecs,
                dx,dy,dz,
                roll,pitch,yaw
            ])
            print(f"Logged data to {self.error_filename}")

        return

    def pose_callback(self, file_name, msg):
        #Callback function for the PoseStamped message.

        # Convert quaternions to euler
        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w

        roll, pitch, yaw = np.degrees(tft.euler_from_quaternion([qx,qy,qz,qw]))

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
        self.filter_pose.position.x = msg.pose.pose.position.x
        self.filter_pose.position.y = msg.pose.pose.position.y
        self.filter_pose.position.z = msg.pose.pose.position.z
        self.filter_pose.orientation.x = msg.pose.pose.orientation.x
        self.filter_pose.orientation.y = msg.pose.pose.orientation.y
        self.filter_pose.orientation.z = msg.pose.pose.orientation.z
        self.filter_pose.orientation.w = msg.pose.pose.orientation.w
        self.pose_callback(self.filter_filename, msg)
        return

    def ground_truth_callback(self, msg):
        self.header = msg.header
        self.ground_truth_pose.position.x = msg.pose.pose.position.x
        self.ground_truth_pose.position.y = msg.pose.pose.position.y
        self.ground_truth_pose.position.z = msg.pose.pose.position.z
        self.ground_truth_pose.orientation.x = msg.pose.pose.orientation.x
        self.ground_truth_pose.orientation.y = msg.pose.pose.orientation.y
        self.ground_truth_pose.orientation.z = msg.pose.pose.orientation.z
        self.ground_truth_pose.orientation.w = msg.pose.pose.orientation.w

        q = self.filter_pose.orientation
        quaternions_filter = [q.x, q.y, q.z, q.w]
        q_inv = tft.quaternion_inverse(quaternions_filter)

        q = self.ground_truth_pose.orientation
        quaternions_ground_truth = [q.x, q.y, q.z, q.w]

        q_error = tft.quaternion_multiply(quaternions_ground_truth, q_inv)

        roll, pitch, yaw = np.degrees(tft.euler_from_quaternion(q_error))

        dx = self.ground_truth_pose.position.x - self.filter_pose.position.x
        dy = self.ground_truth_pose.position.y - self.filter_pose.position.y
        dz = self.ground_truth_pose.position.z - self.filter_pose.position.z

        # Write to csv
        with open(self.error_filename, mode="a") as file:
            writer = csv.writer(file)
            writer.writerow([
                self.header.stamp.secs,
                self.header.stamp.nsecs,
                dx,dy,dz,
                roll,pitch,yaw
            ])
            print(f"Logged data to {self.error_filename}")

        self.pose_callback(self.ground_truth_filename, msg)
        return

if __name__ == "__main__":
    """Initializes the ROS node and subscriber."""
    rospy.init_node("pose_logger", anonymous=True)

    csv_generator = DataGenerator()

    test = bag_files[9]
    bag_file = os.path.join(path, test)

    print("Starting rosbag playback...")
    process = subprocess.Popen(["rosbag", "play", bag_file])

    csv_generator.initialize(test)

    rospy.loginfo("Waiting for rosbag to finish...")
    while process.poll() is None and not rospy.is_shutdown():
        rospy.sleep(0.1)


#    rospy.spin()

