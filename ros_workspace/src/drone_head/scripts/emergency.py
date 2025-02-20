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

#Bigger radius than normal waypoint
radius = 5

#margins of error
x_margin = 0.04
y_margin = 0.04
z_margin = 0.01

#half side length of april tag
half_side_length = 0.05

#distance to ascend to dock
ascend_length_to_dock =0.2
ascend_margin = 0.01

#docking done
done = False

#distance between tag 0/1 and docking station
length_to_dock = 0.35

drone_roll = 0
drone_pitch = 0
drone_yaw = 0

tag_position = Vector3()
tag_orientation = Orientation()

#MEMORY DATA
last_waypoint = XYZYaw()
last_time = 0
empty = True

#Get main detection. calculate waypoint and save it untill needed.
def calculate(data):


    silenceErrors.suppress_TF_REPEATED_DATA()

    global tag_position, tag_orientation, last_waypoint
    global radius,z_margin,x_margin,length_to_dock, done, ascend_length_to_dock

    #Extract Position from Data
    tag_position.x = data.pose.pose.pose.position.x
    tag_position.y = data.pose.pose.pose.position.y
    tag_position.z = data.pose.pose.pose.position.z

    # Extract the orientation (as quaternion)
    orientation_q = data.pose.pose.pose.orientation

    # Convert quaternion to roll, pitch, yaw
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (tag_orientation.roll, tag_orientation.pitch, tag_orientation.yaw) = tf.transformations.euler_from_quaternion(orientation_list)

    # Get Time 
    llast_time = data.pose.header.stamp.to_sec()

    #Set Flag
    empty = False

    id = data.id[0]


    if done:
        return
    
    #Tag 1 or 0
    if(id <= 1):
            angle = tag_orientation.yaw 
            
            #account for difference between tag 1 and 0
            if(id == 0):
                tag_position.x += -0.000037
                tag_position.y += -0.005402
                tag_position.z += -0.00449
            
            #if drone is aligned in Y with docking station. approach it 
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

            
    #tag 3
    elif(id == 3):
            angle = 0.1



            local_pose = geometry_msgs.msg.Pose()
            local_pose.position.x = tag_position.x + (radius * sin(tag_orientation.yaw))
            local_pose.position.y = tag_position.y  + (radius * cos(-tag_orientation.yaw))
            local_pose.position.z = tag_position.z 

            quaternion = quaternion_from_euler(0, 0, -(tag_orientation.yaw + math.pi/2))
    
            local_pose.orientation.x = quaternion[0]
            local_pose.orientation.y = quaternion[1]
            local_pose.orientation.z = quaternion[2]
            local_pose.orientation.w = quaternion[3]

           


    #tag 4
    else:
            if(id == 4):
                if(tag_orientation.yaw>=0):
                    angle = -0.1
                else:
                    angle = 0.1
            else:
                angle = -0.1

            
            local_pose = geometry_msgs.msg.Pose()
            local_pose.position.x = (tag_position.x + radius* sin(-tag_orientation.yaw)) 
            local_pose.position.y = (tag_position.y -  (radius * cos(-tag_orientation.yaw)))
            local_pose.position.z = tag_position.z 
            
            quaternion = quaternion_from_euler(0, 0, (tag_orientation.yaw + math.pi/2))
            local_pose.orientation.x = quaternion[0]
            local_pose.orientation.y = quaternion[1]
            local_pose.orientation.z = quaternion[2]
            local_pose.orientation.w = quaternion[3]

          
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

    if(id<=1):
            
            if(abs(tag_position.x - (radius))<x_margin and abs(tag_position.y)<y_margin ):

                vector_msg.z+=ascend_length_to_dock 
                """ rospy.loginfo("Tag z:" + str(tag_position.z) + "THem plus eachother" + str(tag_position.z + ascend_length_to_dock))
                if(tag_position.z + ascend_length_to_dock <ascend_margin): """
                """ docking_done.publish(0.0)
                done = True """
                """  return """

    

        # Populate the message
    last_waypoint.XYZ.x = vector_msg.x
    last_waypoint.XYZ.y = vector_msg.y
    last_waypoint.XYZ.z = vector_msg.z
    last_waypoint.Yaw.data = angle

    rospy.loginfo("")   

def activated(data):
    global empty,last_time,last_waypoint
    value = data.data
    current_time = rospy.Time.now().to_sec()
    if(data == 0):
          return
    elif(not empty ):
            if((current_time-last_time<10) and (current_time-last_time>5)):
                pubXYZYAW = rospy.Publisher('/set_XYZYaw_waypoint', XYZYaw, queue_size=10)
                pubXYZYAW.publish(last_waypoint)
                empty = True
    else:
            search_activate = rospy.Publisher('search_activate', Float64, queue_size=10)
            search_activate.publish(1)
                   
     
def done_callback(data):
    global done
    # Set 'done' to True if data received is 1, otherwise False
    done = True if data.data == 1.0 else False

if __name__ == "__main__":

    rospy.init_node('emergency')
    silenceErrors.suppress_TF_REPEATED_DATA()

    main_detection_sub=rospy.Subscriber("/main_detection", AprilTagDetection, callback=calculate)
    activate_emergency_sub=rospy.Subscriber("/activate_emergency", Float64, callback=activated)
    rospy.Subscriber('docking_done', Float64, done_callback)

    rospy.spin()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        message = "hi"
        rate.sleep()