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
import csv

apriltag_pose = Pose()

def euclidean_distance(pose1, pose2):
    # Calculate Euclidean distance from the origin.
    return math.sqrt((pose1.x-pose2.x)**2 + (pose1.y-pose2.y)**2 + (pose1.z-pose2.z)**2)

def save_csv(drones):
    # Choose the drone with the longest time array to sample indices
    longest_time_array = max(drones, key=lambda d: len(d.time_array)).time_array

    if len(longest_time_array) < 4:
        print("Not enough data points to sample 4 times.")
        return

    # Pick 4 evenly spaced indices
    total = len(longest_time_array)
    indices = [int(i * total / 4) for i in range(4)]

    with open("priority_snapshots.csv", "w", newline='') as file:
        writer = csv.writer(file)

        # Extended header
        writer.writerow(["Time (s)", 
                         "First priority", "", "", "", "", 
                         "Second priority", "", "", "", "", 
                         "Third priority", "", "", "", ""])
        writer.writerow(["", 
                         "Drone", "Score", "Distance (m)", "Battery (%)", "Memory (%)", 
                         "Drone", "Score", "Distance (m)", "Battery (%)", "Memory (%)", 
                         "Drone", "Score", "Distance (m)", "Battery (%)", "Memory (%)"])

        for idx in indices:
            snapshot = []
            t = longest_time_array[idx]
            snapshot.append(f"{t:.2f}")

            entries = []
            for drone in drones:
                i = idx if len(drone.time_array) > idx else -1
                entries.append((
                    drone.drone_name,
                    drone.deadline_array[i],
                    drone.distance_array[i],
                    drone.battery_array[i],
                    drone.memory_array[i]
                ))

            # Sort by score descending
            entries.sort(key=lambda x: x[1], reverse=True)

            # Write top 3
            for entry in entries[:3]:
                name, score, distance, battery, memory = entry
                snapshot.extend([
                    name, 
                    f"{score:.3f}", 
                    f"{distance:.2f}", 
                    f"{battery:.1f}", 
                    f"{memory:.1f}"
                ])

            writer.writerow(snapshot)

    print("Saved priority snapshots to 'priority_snapshots.csv'.")


class Drone():
    def __init__(self, drone_name, battery_left=100, memory_left=100):
        self.total_battery       = 100   # percentage 2700  # mAh
        self.total_memory        = 100   # percentage 256   # GB
        self.total_distance      = 10 # m
        
        self.battery_left         = battery_left
        self.battery_initial      = battery_left
        #self.consumption_rate    = 0.1/60
        #self.speed               = 0.1
        #self.charging_duration   = 0
        self.distance_to_charger  = 0
        self.memory_initial       = memory_left
        self.memory_left          = memory_left

        self.drone_name = drone_name

        # self.time_to_reach_charger = self.distance_to_charger / self.speed

        # self.start_time = rospy.Time.now().to_sec()
        self.effective_deadline = 0

        self.time_array     = []
        self.deadline_array = []
        self.battery_array  = []
        self.memory_array   = []
        self.distance_array = []

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

        self.distance_to_charger = round(euclidean_distance(apriltag_pose.position, msg.pose.pose.position),3)
        # print(apriltag_pose)

        if already_moved == 1:
            if not hasattr(self, 'start_time') or self.start_time is None:
                self.start_time = msg.header.stamp.to_sec()

            t = msg.header.stamp.to_sec() - self.start_time

            #t = rospy.Time.now().to_sec() - self.start_time
            self.battery_left = round(self.battery_initial - 6.25*t,3)
            self.memory_left  = round(self.memory_initial  - 2*t,3)

            # self.battery_left = self.battery_initial
            # self.memory_left = self.memory_initial

            self.calculate_deadline()
        else:
            t = 0

        if self.battery_left < 0:
            self.battery_left = 0
            rospy.signal_shutdown("No battery left")

        if self.memory_left < 0:
            self.memory_left = 0
            rospy.signal_shutdown("No storage left")

        if self.distance_to_charger > self.total_distance+1 or self.distance_to_charger <= 0.5:
            rospy.signal_shutdown("No storage left")

        self.time_array.append(t)
        self.deadline_array.append(self.effective_deadline)
        self.distance_array.append(self.distance_to_charger)
        self.battery_array.append(self.battery_left)
        self.memory_array.append(self.memory_left)

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
        rospy.sleep(1)
        self.pub.publish(pose_msg)
        return

def apriltag_callback(msg):
    global apriltag_pose
    apriltag_pose = msg.pose.pose
    return

def plot(hummingbird, hummingbird1, hummingbird2):
    print("Shutting down and saving plot...")

    drones = [hummingbird, hummingbird1, hummingbird2]

    for drone in drones:
        # Find the first index with a non-zero time
        non_zero_idx = next((i for i, t in enumerate(drone.deadline_array) if t > 0), None)
        drone.time_array     = drone.time_array[non_zero_idx:]
        drone.deadline_array = drone.deadline_array[non_zero_idx:]
        drone.battery_array  = drone.battery_array[non_zero_idx:]
        drone.memory_array   = drone.memory_array[non_zero_idx:]

    # Save CSV snapshots
    save_csv(drones)

    plt.figure()
    for drone in drones:
        diff = np.shape(drone.deadline_array)[0] - np.shape(drone.time_array)[0]
        print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{diff}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if diff > 0:
            drone.deadline_array = drone.deadline_array[:-diff]
        elif diff < 0:
            drone.time_array = drone.time_array[:-abs(diff)]      
        plt.plot(drone.time_array, drone.deadline_array, label=drone.drone_name)

    # plt.title("Data Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Priority score")
    plt.legend()
    plt.savefig("ros_plot.png", dpi=300, bbox_inches='tight')
    # Optional: show plot at shutdown (will block!)

    # plt.show()

if __name__ == '__main__':
    rospy.on_shutdown(lambda: plot(hummingbird, hummingbird1, hummingbird2))

    rospy.init_node("coordination_simulation")
    rospy.Subscriber("/apriltag_box/real_odometry_sensor/odometry", Odometry, apriltag_callback)

    hummingbird  = Drone(drone_name="hummingbird_1", battery_left=100, memory_left=80)
    hummingbird1 = Drone(drone_name="hummingbird_2", battery_left=70, memory_left=90) 
    hummingbird2 = Drone(drone_name="hummingbird_3", battery_left=85, memory_left=70) 

    move = 1
    already_moved = 0
    if move:
        hummingbird.move((1,0,2))       # 1
        hummingbird1.move((0,10,2))      # 10
        hummingbird2.move((-5,0,2))     # -5
        rospy.sleep(3)
        already_moved = 1

    rospy.sleep(3)

    step = 2

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        hummingbird.move((step,0,2))
        hummingbird1.move((0,11-step,2))

        print(f"---------\nDistance;\n{hummingbird.drone_name}: {hummingbird.distance_to_charger} {hummingbird1.drone_name}: {hummingbird1.distance_to_charger} {hummingbird2.drone_name}: {hummingbird2.distance_to_charger}\n")
        print(f"Battery:\n{hummingbird.drone_name}: {hummingbird.battery_left} {hummingbird1.drone_name}: {hummingbird1.battery_left} {hummingbird2.drone_name}: {hummingbird2.battery_left}\n")
        print(f"Memory:\n{hummingbird.drone_name}: {hummingbird.memory_left} {hummingbird1.drone_name}: {hummingbird1.memory_left} {hummingbird2.drone_name}: {hummingbird2.memory_left}\n---------")

        step += 1

        rate.sleep() 
