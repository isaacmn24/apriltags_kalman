#!/usr/bin/env python3

import rospy
from apriltag_ros.msg import AprilTagDetection, AprilTagDetectionArray
from gazebo_msgs.msg import ModelStates
import geometry_msgs.msg
from geometry_msgs.msg import PoseStamped, Twist, Pose, Vector3, Vector3Stamped,PointStamped
from math import atan2, cos, sin, radians, degrees
from std_msgs.msg import String, Float64, Header
from tf.transformations import quaternion_from_euler, quaternion_multiply, euler_from_quaternion, euler_matrix, quaternion_from_euler
from time import sleep
import logging
import math
import silenceErrors
import tf
import tf.transformations
import numpy as np
import tf2_geometry_msgs
import tf2_ros
import random
from drone_relative_position_cascaded_pid_controller.msg import XYZYaw, model_kinematics, waypoint_kinematics


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

#radius of rotation
radius = 2.5

#margins of error
x_margin = 0.04
y_margin = 0.04
z_margin = 0.01

#half side length of tag
half_side_length = 0.05

#height we have to ascend to dock
ascend_length_to_dock =0.2
ascend_margin = 0.01

#procedure done?
done = False

#length between docking station and tag 1/0
length_to_dock = 0.35


#drone info
drone_roll = 0
drone_pitch = 0
drone_yaw = 0

#tag info
tag_position = Vector3()
tag_orientation = Orientation()

#MEMORY DATA
last_waypoint = PoseStamped()

def calculate(data):
    
    silenceErrors.suppress_TF_REPEATED_DATA()

    global tag_position, tag_orientation,last_waypoint
    global radius,z_margin,x_margin,length_to_dock, done, ascend_length_to_dock

    #Extract Position from Data
    tag_position.x = data.pose.pose.pose.position.x
    tag_position.y = data.pose.pose.pose.position.y
    tag_position.z = data.pose.pose.pose.position.z

    #Extract the orientation (as quaternion)
    orientation_q = data.pose.pose.pose.orientation

    #Convert quaternion to roll, pitch, yaw
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (tag_orientation.roll, tag_orientation.pitch, tag_orientation.yaw) = tf.transformations.euler_from_quaternion(orientation_list)

    search_activate = rospy.Publisher('search_activate', Float64, queue_size=10)

    #PUBLISH Motion
    pubXYZYAW = rospy.Publisher('/set_XYZYaw_waypoint', XYZYaw, queue_size=10)
    docking_done = rospy.Publisher('docking_done', Float64, queue_size=10)

    id = data.id[0]

    #docking is done.
    if done:
        return
    
    #ID 0 or 1
    if(id <= 1):
            angle = -tag_orientation.yaw 

            last_waypoint.header = Header()
            last_waypoint.header = data.pose.header
            
            
            #account for difference between tag 1 and 0
            if(id == 0):
                tag_position.x += -0.000037
                tag_position.y += -0.005402
                tag_position.z += -0.00449

            if(abs(tag_position.y)<y_margin/5):
                radius = length_to_dock

            local_pose = geometry_msgs.msg.Pose()
            local_pose.position.x = tag_position.x - (radius  * abs(cos(-angle)))
            local_pose.position.y = tag_position.y + (radius  * sin(-angle))
            local_pose.position.z = tag_position.z 
            
            quaternion =  quaternion_from_euler(0, 0, angle)
            local_pose.orientation.x = quaternion[0]
            local_pose.orientation.y = quaternion[1]
            local_pose.orientation.z = quaternion[2]
            local_pose.orientation.w = quaternion[3]

            
            last_waypoint.pose = local_pose
    #Tag 3    
    elif(id == 3):
            angle = 0.1

            last_waypoint.header = Header()
            last_waypoint.header = data.pose.header


            local_pose = geometry_msgs.msg.Pose()
            local_pose.position.x = tag_position.x + (radius * sin(tag_orientation.yaw))
            local_pose.position.y = tag_position.y  + (radius * cos(-tag_orientation.yaw))
            local_pose.position.z = tag_position.z 

            quaternion = quaternion_from_euler(0, 0, -(tag_orientation.yaw + math.pi/2))
    
            local_pose.orientation.x = quaternion[0]
            local_pose.orientation.y = quaternion[1]
            local_pose.orientation.z = quaternion[2]
            local_pose.orientation.w = quaternion[3]

           

            last_waypoint.pose = local_pose

    #Tag 4
    else:
            
            if(tag_orientation.yaw>=0):
                    angle = 0.1
            else:
                    angle = -0.1
           

            last_waypoint.header = Header()
            last_waypoint.header = data.pose.header

            
            local_pose = geometry_msgs.msg.Pose()
            local_pose.position.x = (tag_position.x + radius* sin(-tag_orientation.yaw)) 
            local_pose.position.y = (tag_position.y -  (radius * cos(-tag_orientation.yaw)))
            local_pose.position.z = tag_position.z 
            
            quaternion = quaternion_from_euler(0, 0, (tag_orientation.yaw + math.pi/2))
            local_pose.orientation.x = quaternion[0]
            local_pose.orientation.y = quaternion[1]
            local_pose.orientation.z = quaternion[2]
            local_pose.orientation.w = quaternion[3]

            last_waypoint.pose = local_pose
    
    toGo = Pose()
    toGo.position = tag_position
    toGo.position.x -= (radius) * abs(cos(angle))
    toGo.position.y -= (radius) * sin(angle)

    """ if(abs(toGo.position.z) < abs(z_margin)):
            toGo.position.z = 0
    if(abs(toGo.position.x) < abs(x_margin)):
            toGo.position.x = 0
    if(abs(toGo.position.y) < abs(y_margin)):
            toGo.position.y = 0
    """

    vector_msg = Vector3((toGo.position.x ) ,(toGo.position.y), (toGo.position.z))

    #Check if it should ascend to dock
    if(id<=1):
            
            if(abs(tag_position.x - (radius))<x_margin and abs(tag_position.y)<y_margin ):

                vector_msg.z+=ascend_length_to_dock 
                """ rospy.loginfo("Tag z:" + str(tag_position.z) + "THem plus eachother" + str(tag_position.z + ascend_length_to_dock))
                if(tag_position.z + ascend_length_to_dock <ascend_margin): """
                docking_done.publish(0.0)
                done = True
                """  return """

    waypoint = XYZYaw()

    #Populate the message
    waypoint.XYZ.x = vector_msg.x
    waypoint.XYZ.y = vector_msg.y
    waypoint.XYZ.z = vector_msg.z
    waypoint.Yaw.data = angle
        
    pubXYZYAW.publish(waypoint)

    rospy.loginfo("")   


if __name__ == "__main__":

    rospy.init_node('waypoint_calculator')
    silenceErrors.suppress_TF_REPEATED_DATA()

    sub=rospy.Subscriber("/main_detection", AprilTagDetection, callback=calculate)
    


    rospy.spin()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        message = "hi"
        rate.sleep()