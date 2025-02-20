#!/usr/bin/env python3

import rospy
from apriltag_ros.msg import AprilTagDetection, AprilTagDetectionArray
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Pose, Vector3
from math import atan2, cos, sin, radians, degrees
from std_msgs.msg import Float64
from tf.transformations import euler_from_quaternion
from time import sleep
import silenceErrors
import tf
import tf.transformations
import numpy as np


#DEFINE ACTUAL ORIENTATION AND POSITION OF APRIL TAG
main_detection_pub = rospy.Publisher('/main_detection', AprilTagDetection, queue_size=10)

class Orientation:
    def _init_(self, roll=0.0, pitch=0.0, yaw=0.0):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
    
    def update(self, delta_roll, delta_pitch, delta_yaw):
        self.roll += delta_roll
        self.pitch += delta_pitch
        self.yaw += delta_yaw
    
    def set_angles(self, roll, pitch, yaw):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

#Tag Position
tag_position = Vector3()

#Tag Orientation
tag_orientation = Orientation()
drone_roll = 0
drone_pitch = 0
drone_yaw = 0

#Half Side Length of each tag 
half_side_length = 0.05

def rotation_matrix(roll, pitch, yaw):
    # Roll matrix
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]]) 
    # Pitch matrix
    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])
    # Yaw matrix
    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])
    # Combined rotation matrix
    R = np.dot(R_z, np.dot(R_y, R_x))
    return R

def transformTagPose(pose):
    global tag_position, tag_orientation,drone_roll,drone_pitch,drone_yaw
    tag_position = Vector3((pose.position.z ) ,(-1 * pose.position.x), (-1 * pose.position.y))
    
    
    (tag_roll,  tag_pitch,  tag_yaw) = euler_from_quaternion(
                [pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w]
        )
    
    R = rotation_matrix(drone_roll, drone_pitch, 0)

    tag_position_np = np.array([tag_position.x, tag_position.y, tag_position.z])

    tag_position.x,tag_position.y,tag_position.z = np.dot(R, tag_position_np)

    tag_roll = tag_roll
    tag_pitch = tag_pitch
    tag_yaw = tag_yaw
    tag_orientation.set_angles(tag_roll,tag_yaw, tag_pitch )

    tag_position.x += half_side_length * cos(tag_orientation.yaw)
    tag_position.y += half_side_length * sin(tag_orientation.yaw) 

def reader(data):
    silenceErrors.suppress_TF_REPEATED_DATA()

    global tag_position, tag_orientation

    detections = data.detections
    search_activate = rospy.Publisher('search_activate', Float64, queue_size=10)

    if (len(detections) > 0 ) :
        
        #Reset search counter
        search_activate.publish(0)

        #Loop through detections to get one with lowest ID        
        main_detection = detections[0]
        main_id = detections[0].id

        for detection in detections:
            if detection.id[0]<=main_id[0]:
                main_detection = detection
                main_id = detection.id
        

        #Transfrom
        transformTagPose(main_detection.pose.pose.pose)
        quaternion = tf.transformations.quaternion_from_euler(tag_orientation.roll, tag_orientation.pitch, tag_orientation.yaw)
        main_detection.pose.pose.pose.position = tag_position

        #Set the orientation using the quaternion
        main_detection.pose.pose.pose.orientation.x = quaternion[0]
        main_detection.pose.pose.pose.orientation.y = quaternion[1]
        main_detection.pose.pose.pose.orientation.z = quaternion[2]
        main_detection.pose.pose.pose.orientation.w = quaternion[3]

        #Publish it to other nodes
        
        main_detection_pub.publish(main_detection)

    else:
        emergency_pub = rospy.Publisher('/activate_emergency', Float64, queue_size=10)
        emergency_pub.publish(1)
        return


def tag_side_length_callback(msg):
    global half_side_length
    half_side_length = msg.data/2


def get_drone_pose(msg):

    global drone_roll,drone_pitch,drone_yaw
    quaternion = (
        msg.orientation.x,
        msg.orientation.y,
        msg.orientation.z,
        msg.orientation.w
    )

    # Convert the quaternion to roll, pitch, yaw
    drone_roll,drone_pitch,drone_yaw = tf.transformations.euler_from_quaternion(quaternion)


if __name__ == "__main__":

    rospy.init_node('read')
    silenceErrors.suppress_TF_REPEATED_DATA()

    sub=rospy.Subscriber("/tag_detections", AprilTagDetectionArray, callback=reader)
    rospy.Subscriber('/hummingbird/odometry_sensor1/pose', Pose, get_drone_pose)


    rospy.Subscriber('/tag_side_length', Float64, tag_side_length_callback)


    rospy.spin()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        message = "hi"
        rate.sleep()