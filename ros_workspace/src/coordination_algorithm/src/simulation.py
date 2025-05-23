#!/usr/bin/env python

import rospy
import tf2_ros
import tf.transformations as tft
import tf2_geometry_msgs
from geometry_msgs.msg import PoseStamped, Transform, Twist, Pose, Quaternion
from nav_msgs.msg import Odometry
from trajectory_msgs.msg import MultiDOFJointTrajectory, MultiDOFJointTrajectoryPoint
import math
import numpy as np
import matplotlib.pyplot as plt

apriltag_pose = Pose()

def euclidean_distance(pose1, pose2):
    # Calculate Euclidean distance from the origin.
    return math.sqrt((pose1.x-pose2.x)**2 + (pose1.y-pose2.y)**2 + (pose1.z-pose2.z)**2)

class Drone():
    def __init__(self, drone_name, battery_left=100, memory_left=100):
        self.total_battery       = 100   # percentage 2700  # mAh
        self.total_memory        = 100   # percentage 256   # GB
        self.total_distance      = 10 # m
        
        self.battery_left        = battery_left
        #self.consumption_rate    = 0.1/60
        #self.speed               = 0.1
        #self.charging_duration   = 0
        self.distance_to_charger = 0
        self.memory_left         = memory_left

        self.drone_name = drone_name

        # self.time_to_reach_charger = self.distance_to_charger / self.speed

        self.start_time = rospy.Time.now().to_sec()
        self.effective_deadline = 0

        self.time_array     = []
        self.deadline_array = []
        self.battery_array  = []
        self.memory_array   = []

        number_of_priorities = 3
        self.w_battery  = 1 / number_of_priorities
        self.w_distance = 1 / number_of_priorities
        self.w_memory   = 1 / number_of_priorities

        self.drone_pose = PoseStamped()

        self.sub = rospy.Subscriber(f'/{self.drone_name}/real_odometry_sensor/odometry', Odometry, self.odom_callback)
        self.pub = rospy.Publisher(f'/{self.drone_name}/command/pose', PoseStamped, queue_size=10)

        return

    def odom_callback(self, msg):
        self.drone_pose.header = msg.header
        self.drone_pose.pose = msg.pose.pose

        self.distance_to_charger = euclidean_distance(apriltag_pose.position, msg.pose.pose.position)
        # print(apriltag_pose)

        t = rospy.Time.now().to_sec() - self.start_time
        battery_left = 100 - 6.25*t
        memory_left  = 100 - 2*t

        if battery_left < 0:
            self.battery_left = 0
            rospy.signal_shutdown("No battery left")
        else:
            self.battery_left = battery_left

        # if memory_left < 0:
        #     print("Memoria acabada")
        #     self.memory_left = 0
        # else:
        #     self.memory_left = memory_left

        self.time_array.append(t)
        self.deadline_array.append(self.effective_deadline)
        self.battery_array.append(self.battery_array)
        self.memory_array.append(self.memory_array)

        return

    def calculate_deadline(self):
    	# Slack is the amount of time a task can be delayed before it must start in order to meet its deadline. Juego, de toda la vida
        # slack = (self.battery_left / self.consumption_rate) - self.time_to_reach_charger - self.charging_duration

        # For FCFS when a drone is under 15% it just sends signal and whichever
        # wants first, comes first
        # FCFS = self.battery_left

        normal_battery  = 1 - self.battery_left/self.total_battery
        normal_distance = self.distance_to_charger/self.total_distance
        normal_memory   = 1 - self.memory_left/self.total_memory

        self.effective_deadline = self.w_battery * normal_battery + self.w_distance * normal_distance + self.w_memory * normal_memory
        return self.effective_deadline

    def move(self, waypoint):
        print(f"Moving drone {self.drone_name} to {waypoint}")

        # Create the message
        pose_msg = PoseStamped()
        pose_msg.header = self.drone_pose.header

        pose_msg.pose.position.x = waypoint[0]
        pose_msg.pose.position.y = waypoint[1]
        pose_msg.pose.position.z = waypoint[2]

        pose_msg.pose.orientation.w = 1

        # Send the message
        rospy.sleep(2)  # Give time for publisher to register
        self.pub.publish(pose_msg)
        #rospy.sleep(5)
        return

def apriltag_callback(msg):
    global apriltag_pose
    apriltag_pose = msg.pose.pose
    return

def plot(hummingbird, hummingbird1, hummingbird2):
        print("Shutting down and saving plot...")

        drones = [hummingbird, hummingbird1, hummingbird2]

        plt.figure()
        for drone in drones:
            plt.plot(drone.time_array, drone.deadline_array, label=drone.drone_name)

        plt.title("Data Over Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Value")
        plt.legend()
        plt.savefig("ros_plot.png", dpi=300, bbox_inches='tight')
        # Optional: show plot at shutdown (will block!)

        # plt.show()

if __name__ == '__main__':
    rospy.on_shutdown(lambda: plot(hummingbird, hummingbird1, hummingbird2))

    rospy.init_node("coordination_simulation")
    rospy.Subscriber("/apriltag_box/real_odometry_sensor/odometry", Odometry, apriltag_callback)

    hummingbird  = Drone(drone_name="hummingbird")
    hummingbird1 = Drone(drone_name="hummingbird2")
    hummingbird2 = Drone(drone_name="hummingbird3")

    move = 1
    if move:
        hummingbird.move((5,0,2))
        hummingbird1.move((0,5,2))
        hummingbird2.move((-5,0,2))

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        deadlines = [(hummingbird, hummingbird.calculate_deadline()),
                 (hummingbird1, hummingbird1.calculate_deadline()),
                 (hummingbird2, hummingbird2.calculate_deadline())]
    
        # Sort by highest priority (EDF-like: most urgent = lowest score)
        deadlines.sort(key=lambda x: x[1], reverse=True)

        # Output results
        # print("\n\n\n\nDrone charging priority (highest to lowest):")
        # for drone, score in deadlines:
            # print(f"{drone.drone_name}: \nbattery  = {drone.battery_left}% left \ndistance = {drone.distance_to_charger} m away from charger \nmemory   = {drone.memory_left}% left \n\npriority score = {score:.2f} \n-----------------------------")

        rate.sleep() 

    """def move(self, waypoint):
        # Create the message
        trajectory_msg = MultiDOFJointTrajectory()
        trajectory_msg.joint_names.append("base_link")

        # Define transform (position and orientation)

        target_x = waypoint[0]
        target_y = waypoint[1]
        target_z = waypoint[2]

        transform = Transform()
        transform.translation = Vector3(x=target_x, y=target_y, z=target_z)
        transform.rotation = Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)  # No rotation

        # Define velocity
        velocity = Twist()

        # # Direction from current to target
        # dx = target_x - current_x
        # dy = target_y - current_y
        # dz = target_z - current_z

        # norm = math.sqrt(dx**2 + dy**2 + dz**2)

        # # Desired speed (e.g. 1 m/s)
        # speed = 1.0

        # vx = speed * dx / norm
        # vy = speed * dy / norm
        # vz = speed * dz / norm

        velocity.linear = Vector3(x=0.5, y=0.0, z=0.0)  # 0.5 m/s in x
        velocity.angular = Vector3(x=0.0, y=0.0, z=0.0)

        # Create trajectory point
        point = MultiDOFJointTrajectoryPoint()
        point.transforms.append(transform)
        point.velocities.append(velocity)
        point.time_from_start = rospy.Duration(10.0)  # Reach target in 10 seconds

        # Add point to message
        trajectory_msg.points.append(point)

        # Send the message
        rospy.sleep(1)  # Give time for publisher to register
        self.pub.publish(trajectory_msg)

        return"""