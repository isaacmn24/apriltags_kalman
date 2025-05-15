#!/usr/bin/env python

import rospy
import csv
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, TransformStamped
import tf.transformations
import numpy as np

# Test
test = "top-left"

# Define the CSV file
ground_truth_filename = f"ground_truth_data_{test}.csv"
error_filename = f"error_data_{test}.csv"

# Write the header for the CSV file
with open(ground_truth_filename, mode="w") as file:
    writer = csv.writer(file)
    writer.writerow(["time_secs", "time_nsecs", "x_meas", "y_meas", "z_meas", "roll_meas", "pitch_meas", "yaw_meas"])

# Write the header for the CSV file
with open(error_filename, mode="w") as file:
    writer = csv.writer(file)
    writer.writerow(["time_secs", "time_nsecs", "x_err", "y_err", "z_err", "roll_err", "pitch_err", "yaw_err"])

def pose_callback(file_name, msg):
    """Callback function for the PoseStamped message."""

    if isinstance(msg, PoseWithCovarianceStamped):
        msg.pose = msg.pose.pose

    # Convert quaternions to euler
    qx = msg.transform.rotation.x
    qy = msg.transform.rotation.y
    qz = msg.transform.rotation.z
    qw = msg.transform.rotation.w

    roll, pitch, yaw = np.rad2deg(tf.transformations.euler_from_quaternion([qx,qy,qz,qw]))

    # Write to csv
    with open(file_name, mode="a") as file:
        writer = csv.writer(file)
        writer.writerow([
            msg.header.stamp.secs,
            msg.header.stamp.nsecs,
            msg.transform.translation.x,
            msg.transform.translation.y,
            msg.transform.translation.z,
            roll,pitch, yaw
        ])
        print(f"Logged data to {file_name}")

def error_callback(msg):
    pose_callback(error_filename, msg)

def ground_truth_callback(msg):
    pose_callback(ground_truth_filename, msg)

if __name__ == "__main__":
    """Initializes the ROS node and subscriber."""
    rospy.init_node("pose_logger", anonymous=True)

    rospy.Subscriber("/apriltag/transformed_pose/ground_truth", TransformStamped, ground_truth_callback)
    rospy.Subscriber("/apriltag/transformed_pose/error", TransformStamped, error_callback)

    rospy.spin()