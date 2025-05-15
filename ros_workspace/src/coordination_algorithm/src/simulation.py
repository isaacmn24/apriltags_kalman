#!/usr/bin/env python

import rospy
import tf2_ros
import tf.transformations as tft
import tf2_geometry_msgs
from geometry_msgs.msg import PoseStamped, Transform, Twist, Vector3, Quaternion
from nav_msgs.msg import Odometry
from trajectory_msgs.msg import MultiDOFJointTrajectory, MultiDOFJointTrajectoryPoint
import math
import numpy as np

class Drone():
    def __init__(self, drone_name, battery_left, distance_to_charger, memory_left):
        self.battery_left        = battery_left
        self.consumption_rate    = 0.1/60
        self.speed               = 0.1
        self.charging_duration   = 0
        self.distance_to_charger = distance_to_charger
        self.memory_left         = memory_left

        self.drone_name = drone_name

        self.time_to_reach_charger = self.distance_to_charger / self.speed

        number_of_priorities = 3
        self.w_battery  = 1 / number_of_priorities
        self.w_distance = 1 / number_of_priorities
        self.w_memory   = 1 / number_of_priorities

        # self.pub = rospy.Publisher(f'/{self.drone_name}/command/trajectory', MultiDOFJointTrajectory, queue_size=10)

        return
    
    def calculate_deadline(self):
        time_deadline = (self.battery_left / self.consumption_rate) - self.time_to_reach_charger - self.charging_duration

        effective_deadline = self.w_battery * self.battery_left
        + self.w_distance * self.distance_to_charger
        + self.w_memory * self.memory_left

        return effective_deadline

    def move(self, waypoint):
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

        return

def schedule(drones_deadlines):
    return


if __name__ == '__main__':
    # rospy.init_node("coordination_simulation")

    hummingbird = Drone(drone_name="hummingbird",
                        battery_left=70,
                        distance_to_charger=2,
                        memory_left=60)
    hummingbird1 = Drone(drone_name="hummingbird1",
                        battery_left=20,
                        distance_to_charger=6,
                        memory_left=80)
    hummingbird2 = Drone(drone_name="hummingbird2",
                        battery_left=100,
                        distance_to_charger=20,
                        memory_left=50)

    deadlines = [(hummingbird.drone_name, hummingbird.calculate_deadline()),
                 (hummingbird1.drone_name, hummingbird1.calculate_deadline()),
                 (hummingbird2.drone_name, hummingbird2.calculate_deadline())]
    
    # Sort by highest priority (EDF-like: most urgent = lowest score)
    deadlines.sort(key=lambda x: x[1], reverse=True)

    # Output results
    print("Drone charging priority (highest to lowest):")
    for drone, score in deadlines:
        print(f"{drone}: priority score = {score:.2f}")

    # rate = rospy.Rate(10)  # 10 Hz
    # while not rospy.is_shutdown():

    #     rate.sleep() 