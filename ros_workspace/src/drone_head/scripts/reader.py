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

radius = 2.5

x_margin = 0.04
y_margin = 0.04
z_margin = 0.01

half_side_length = 0.05

ascend_length_to_dock =0.2
ascend_margin = 0.01

done = False

yaw_margin = 0.001

length_to_dock = 0.35

drone_roll = 0
drone_pitch = 0
drone_yaw = 0

#DEFINE ACTUAL ORIENTATION AND POSITION OF APRIL TAG

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
    
tag_position = Vector3()
tag_orientation = Orientation()

#MEMORY DATA
last_waypoint = PoseStamped()

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

    global tag_position, tag_orientation,last_waypoint
    global radius,z_margin,x_margin,length_to_dock, done, ascend_length_to_dock, yaw_margin

    detections = data.detections
    search_activate = rospy.Publisher('search_activate', Float64, queue_size=10)

    # PUBLISH Motion
    pubX = rospy.Publisher('set_x_waypoint', Float64, queue_size=10)
    pubY = rospy.Publisher('set_y_waypoint', Float64, queue_size=10)
    pubZ = rospy.Publisher('set_z_waypoint', Float64, queue_size=10)
    pubYaw = rospy.Publisher('set_yaw_waypoint', Float64, queue_size=10)
    
    pubXYZ = rospy.Publisher('/set_xyz_waypoint', Vector3, queue_size=10)
    pubXYZYAW = rospy.Publisher('/set_XYZYaw_waypoint', XYZYaw, queue_size=10)

    pubXSpeed = rospy.Publisher('set_x_waypoint_speed', Float64, queue_size=10)
    pubYSpeed = rospy.Publisher('set_y_waypoint_speed', Float64, queue_size=10)
    pubZSpeed = rospy.Publisher('set_z_waypoint_speed', Float64, queue_size=10)
    pubYawSpeed = rospy.Publisher('set_yaw_waypoint_speed', Float64, queue_size=10)

    docking_done = rospy.Publisher('docking_done', Float64, queue_size=10)


    if done:
        return

    #or (last_important_detection is not None and (rospy.Time.now().to_sec() -last_important_detection.pose.header.stamp.secs + last_important_detection.pose.header.stamp.nsecs * 1e-9 < 0.0000001))
    if (len(detections) > 0 ) :
        
        search_activate.publish(0)
        
        #last_important_detection is not None and (rospy.Time.now().to_sec() -last_important_detection.pose.header.stamp.secs + last_important_detection.pose.header.stamp.nsecs * 1e-9 < 0.0000001)
        
        main_detection = detections[0]
        main_id = detections[0].id
        

        #get most importatnt tag detected
        for detection in detections:
            if detection.id[0]<=main_id[0]:
                main_detection = detection
                main_id = detection.id
        
        #last_important_detection = main_detection
        

        ##Transfrom to real frame
        transformTagPose(main_detection.pose.pose.pose)
      
        if(main_id[0] <= 1):
            angle = tag_orientation.yaw 

            last_waypoint.header = Header()
            last_waypoint.header = main_detection.pose.header
            
            

            if(main_id[0] == 0):
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
        
        elif(main_id[0] == 3):
            angle = 0.1

            last_waypoint.header = Header()
            last_waypoint.header = main_detection.pose.header


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

          
        else:
            if(main_id[0] == 4):
                if(tag_orientation.yaw>=0):
                    angle = -0.1
                else:
                    angle = 0.1
            else:
                angle = -0.1

            last_waypoint.header = Header()
            last_waypoint.header = main_detection.pose.header

            
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

        if(main_id[0]<=1):
            
            if(abs(tag_position.x - (radius))<x_margin and abs(tag_position.y)<y_margin ):

                vector_msg.z+=ascend_length_to_dock 
                """ rospy.loginfo("Tag z:" + str(tag_position.z) + "THem plus eachother" + str(tag_position.z + ascend_length_to_dock))
                if(tag_position.z + ascend_length_to_dock <ascend_margin): """
                docking_done.publish(0.0)
                done = True
                """  return """

        waypoint = XYZYaw()

        # Populate the message
        waypoint.XYZ.x = vector_msg.x
        waypoint.XYZ.y = vector_msg.y
        waypoint.XYZ.z = vector_msg.z
        waypoint.Yaw.data = angle
        
        pubXYZYAW.publish(waypoint)

        rospy.loginfo("")

    elif last_waypoint.header.stamp is not None and last_waypoint.header.frame_id != "":
        secsSinceLastWaypoint = rospy.Time.now().to_sec() -last_waypoint.header.stamp.secs + last_waypoint.header.stamp.nsecs * 1e-9 
        if(secsSinceLastWaypoint >2 and secsSinceLastWaypoint < 5):
            """ vector_msg = Vector3(last_waypoint.pose.position.x  ,last_waypoint.pose.position.y, last_waypoint.pose.position.z)
        
            pubXYZ.publish(vector_msg)
            #pubYaw.publish(target_yaw)
             """
            

            last_waypoint = PoseStamped()

        else:
            search_activate.publish(1)
    else:
           search_activate.publish(1)
    

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
        
def x_margin_callback(msg):
    global x_margin
    x_margin = msg.data
        

def y_margin_callback(msg):
    global y_margin
    y_margin = msg.data

def z_margin_callback(msg):
    global z_margin
    z_margin = msg.data

def length_to_docking_station_callback(msg):
    global radius
    radius = msg.data

def tag_side_length_callback(msg):
    global half_side_length
    half_side_length = msg.data/2

def height_to_docking_station_callback(msg):
    global ascend_length_to_dock
    ascend_length_to_dock = msg.data

def height_to_docking_station_margin_callback(msg):
    global ascend_margin
    ascend_margin = msg.data

if __name__ == "__main__":

    rospy.init_node('reader')
    silenceErrors.suppress_TF_REPEATED_DATA()

    sub=rospy.Subscriber("/tag_detections", AprilTagDetectionArray, callback=reader)
    rospy.Subscriber('/hummingbird/odometry_sensor1/pose', Pose, get_drone_pose)

    rospy.Subscriber('/x_allowed_margin', Float64, x_margin_callback)
    rospy.Subscriber('/y_allowed_margin', Float64, y_margin_callback)
    rospy.Subscriber('/z_allowed_margin', Float64, z_margin_callback)

    rospy.Subscriber('/length_to_docking_station', Float64, length_to_docking_station_callback)

    rospy.Subscriber('/tag_side_length', Float64, tag_side_length_callback)

    rospy.Subscriber('/height_to_docking_station', Float64, height_to_docking_station_callback)
    rospy.Subscriber('/height_to_docking_station_margin', Float64, height_to_docking_station_margin_callback)


    rospy.spin()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        message = "hi"
        rate.sleep()