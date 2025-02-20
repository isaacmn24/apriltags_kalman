#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from gazebo_msgs.msg import ModelStates
import rospy
import math
import tf2_ros
import math
import tf.transformations
import tf2_geometry_msgs
from time import sleep
from math import radians, degrees
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist, Pose, Vector3, Vector3Stamped
from std_msgs.msg import Float64

class object_kinematics_data:
    def __init__(self):
        # position data: xyz and quaternion
        self.pose = Pose()

        # linear and angular velocities
        self.twist = Twist()
        self.twist.angular = Vector3()
        self.twist.linear = Vector3()

#drone data
drone_absolute_kinematics = object_kinematics_data()
drone_name = "hummingbird"
drone_gazebo_index = 0
obtained_models_index_flag = False

absolute_reference_frame = "world"
desired_reference_frame = drone_name + "/stability_axis"

drone_roll = 0
drone_pitch = 0
drone_yaw = 0


#flag to see if drone should go up or down
goUp = True

#count how many times it has gone up or down to see if it should move in x/y to do spiraling motion
upDownCounter = 0
upDownMax = 2
#max and min Z values
maxZ = 9
minZ = 1

#direction of next spiraling motion
direction = 0

#divide values of motion in Z and rotation 
dividendsPerMeter = 20
#number of rotations of drone per meter around itself
rotationPerMeter = 2



#The time step for the spiral is set to ensure that each motion sequence is completed before the next begins. Since there's no built-in mechanism to queue the waypoints
time_step = 50
#By how much it increases
stepDelta = 20
spiral_timer = 0

#timer to delay search so that it doesn't turn on immediately if a frame is missing apriltags momenterally
timer = 0
timerLimit = 100




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



def obtain_model_indices(gazebo_names_list):
    global drone_gazebo_index
    global obtained_models_index_flag

    for index, name in enumerate(gazebo_names_list):
        if name == drone_name:
            drone_gazebo_index = index
            break
    
    obtained_models_index_flag = True

def gazebo_model_states_callback(states:ModelStates):

    # obtain the indices that we will later on need
    if not obtained_models_index_flag:
        obtain_model_indices(states.name)
    
    # store the absoute data of the drone
    drone_absolute_kinematics.pose.position = states.pose[drone_gazebo_index].position
    drone_absolute_kinematics.pose.orientation = states.pose[drone_gazebo_index].orientation
    drone_absolute_kinematics.twist.angular = states.twist[drone_gazebo_index].angular
    drone_absolute_kinematics.twist.linear = states.twist[drone_gazebo_index].linear


def search(data):
    
    global goUp,upDownCounter,upDownMax,direction,dividendsPerMeter,maxZ,minZ,time_step,stepDelta,timer,timerLimit, rotationPerMeter
    global drone_roll,drone_pitch, drone_yaw, spiral_timer
    
    value = data.data

    if value > 0:

        timer+=1

        if timer>timerLimit:

            pubYaw = rospy.Publisher('set_yaw_waypoint', Float64, queue_size=10)
            pubXYZ = rospy.Publisher('/set_xyz_waypoint', Vector3, queue_size=10)

            #We've reached max or min height:
            if (drone_absolute_kinematics.pose.position.z > maxZ and goUp):
                upDownCounter+=1
                goUp=False
            elif(drone_absolute_kinematics.pose.position.z < minZ and not goUp):
                upDownCounter+=1
                goUp=True
            
            #By default we don't move in X or Y
            x_value = 0
            y_value = 0

            #If we reached the max bounces at this location we start to move in X, Y
            if(upDownCounter==upDownMax):
                if(spiral_timer<0):
                    spiral_timer = time_step
                upDownCounter=0
            
            if (spiral_timer>0):
                
                if(direction == 0):
                    x_value =  spiral_timer * math.cos(drone_yaw)
                    #y_value =  spiral_timer * math.sin(drone_yaw)

                elif(direction == 1):
                    y_value = spiral_timer * math.cos(drone_yaw)
                    #x_value = spiral_timer *( math.sin(drone_yaw))
                elif(direction == 2):
                    x_value = spiral_timer *(-math.cos(drone_yaw))
                    #y_value = spiral_timer *(-math.sin(drone_yaw))
                else:
                    y_value = spiral_timer *(-math.cos(drone_yaw))
                    #x_value = spiral_timer *(-math.sin(drone_yaw))


            elif(spiral_timer == 0):
                if(direction == 0):
                    direction+=1
                elif(direction == 1):
                    time_step+=stepDelta
                    direction+=1
                elif(direction == 2):
                    direction+=1
                else:
                    time_step+=stepDelta
                    direction=0
            spiral_timer-=1
            
            #motion in Z and yaw
            zDelta = 1/dividendsPerMeter if goUp else -1/dividendsPerMeter
            yawDelta = 360 * rotationPerMeter / dividendsPerMeter 

            vector_msg = Vector3(x_value, y_value, zDelta)

            pubXYZ.publish(vector_msg)
            pubYaw.publish(yawDelta)
                
            #rospy.loginfo("current z: %f", drone_absolute_kinematics.pose.position.z)
            #rospy.loginfo("current direction: %f", direction)
            #rospy.loginfo("current step: %f", time_step)
            #rospy.loginfo("Published y position: %f", y_position)
            #rospy.loginfo("Published z position: %f", z_position)

    else:
        timer = 0



    
def timer_before_search_callback(msg):
    global timerLimit
    timerLimit = msg.data

        

if __name__ == "__main__":

    rospy.init_node('search')
    rospy.loginfo("Started.")

    sub=rospy.Subscriber('search_activate', Float64, callback=search)
    #GPSSub=rospy.Subscriber('gps_location', Float64, callback=updateGPS)
    gazebo_subscriber = rospy.Subscriber("/gazebo/model_states", ModelStates, gazebo_model_states_callback)

    rospy.Subscriber('/timer_before_search', Float64, timer_before_search_callback)
    rospy.Subscriber('/hummingbird/odometry_sensor1/pose', Pose, get_drone_pose)


    rospy.spin()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        message = "hi"
        rate.sleep()
