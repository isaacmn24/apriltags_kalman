#!/usr/bin/env python

import rospy
import tf2_ros
import tf.transformations as tft
import tf2_geometry_msgs
from geometry_msgs.msg import PoseStamped, Transform, Twist, Pose, QuaternionStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix
from uav_msgs.msg import uav_pose
import math
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Proj
from pyproj.transformer import Transformer
from std_msgs.msg import Float32, UInt8

apriltag_pose = Pose()

home_gps = (48.750186, 9.105734, 514.354)   # (lat, lon, alt)
object_gps = (48.750272, 9.105765, 537)

# Convert from GPS (LLA) to ECEF
def lla_to_ecef(lat, lon, alt):
    proj_lla = Proj(proj='latlong', datum='WGS84')
    proj_ecef = Proj(proj='geocent', datum='WGS84')

    transformer = Transformer.from_proj(proj_lla, proj_ecef)
    x,y,z = transformer.transform(lon,lat,alt)

    #x,y,z = transform(proj_lla, proj_ecef, lon, lat, alt)
    return np.array([x, y, z])

# Convert ECEF to NED
def ecef_to_ned(ecef_obj, ecef_home, lat_home, lon_home):
    # Convert degrees to radians
    lat_rad = np.radians(lat_home)
    lon_rad = np.radians(lon_home)

    # Translation vector
    dx = ecef_obj - ecef_home

    # ENU rotation matrix
    R_ENU = np.array([
        [-np.sin(lon_rad),              np.cos(lon_rad),             0],
        [-np.sin(lat_rad)*np.cos(lon_rad), -np.sin(lat_rad)*np.sin(lon_rad), np.cos(lat_rad)],
        [np.cos(lat_rad)*np.cos(lon_rad),  np.cos(lat_rad)*np.sin(lon_rad),  np.sin(lat_rad)]
    ])
    R_NED = np.array([
        [-np.sin(lat_rad)*np.cos(lon_rad),   -np.sin(lat_rad)*np.sin(lon_rad),   np.cos(lat_rad)],
        [-np.sin(lon_rad),                          np.cos(lon_rad),                         0],
        [-np.cos(lat_rad)*np.cos(lon_rad),   -np.cos(lat_rad)*np.sin(lon_rad),  -np.sin(lat_rad)]
    ])

    enu = R_NED @ dx
    return enu

def euclidean_distance(pose1, pose2):
    # Calculate Euclidean distance from the origin.
    return math.sqrt((pose1.x-pose2.x)**2 + (pose1.y-pose2.y)**2 + (pose1.z-pose2.z)**2)

class Drone():
    def __init__(self, drone_name):
        self.total_battery       = 100   # percentage 2700  # mAh
        self.total_memory        = 14    # GB
        self.total_distance      = 10 # m
        
        self.battery_left        = 0
        self.distance_to_charger = 0
        self.memory_left         = 0

        self.drone_name = drone_name

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

        self.drone_pose         = PoseStamped()
        self.marker_board_pose  = PoseStamped()

        self.marker_board_sub           = rospy.Subscriber("/fc0/pose", uav_pose, self.marker_board_pose_callback)
        self.drone_pose_vicon_sub       = rospy.Subscriber(f"/{self.drone_name}/drone/gps/location", NavSatFix, self.drone_callback)
        self.drone_attitude_sub         = rospy.Subscriber(f"/{self.drone_name}/drone/attitude", QuaternionStamped, self.drone_attitude_callback)
        self.drone_battery_sub          = rospy.Subscriber(f"/{self.drone_name}/drone/battery", UInt8, self.drone_battery_callback)
        self.drone_storage_sub          = rospy.Subscriber(f"/{self.drone_name}/drone/storage", Float32, self.drone_storage_callback)
        self.drone_storage_capacity_sub = rospy.Subscriber(f"/{self.drone_name}/drone/storage/capacity", Float32, self.drone_storage_capacity_callback)
        
        self.pub = rospy.Publisher(f'/{self.drone_name}/command/pose', PoseStamped, queue_size=10)

        return

    def drone_callback(self,msg):
        """Callback for drone odometry updates"""
        ecef_drone = lla_to_ecef(msg.latitude, msg.longitude, msg.altitude)
        ned = ecef_to_ned(ecef_drone, ecef_home, home_gps[0], home_gps[1])  # result in meters

        self.drone_pose.header          = msg.header
        self.drone_pose.pose.position.x = ned[0]
        self.drone_pose.pose.position.y = ned[1]
        self.drone_pose.pose.position.z = ned[2]

        t = rospy.Time.now().to_sec() - self.start_time

        self.time_array.append(t)
        self.deadline_array.append(self.effective_deadline)
        self.battery_array.append(self.battery_array)
        self.memory_array.append(self.memory_array)

        return
    
    def marker_board_pose_callback(self,msg):
        self.marker_board_pose.header = msg.header
        self.marker_board_pose.pose.orientation = msg.orientation
        self.marker_board_pose.pose.position.x = ned[0]
        self.marker_board_pose.pose.position.y = ned[1]
        self.marker_board_pose.pose.position.z = ned[2]
        return

    def drone_attitude_callback(self,msg):
        self.drone_pose.pose.orientation = msg.quaternion
        return

    def drone_battery_callback(self,msg):
        self.battery_left = msg
        return
    
    def drone_storage_capacity_callback(self,msg):
        self.total_memory = msg
        return
    
    def drone_storage_callback(self,msg):
        self.memory_left = msg
        return

    def calculate_deadline(self):
        self.distance_to_charger = euclidean_distance(self.marker_board_pose.pose.position, self.drone_pose.pose.position)

        normal_battery  = 1 - self.battery_left/self.total_battery
        normal_distance = self.distance_to_charger/self.total_distance
        normal_memory   = 1 - self.memory_left/self.total_memory

        self.effective_deadline = self.w_battery * normal_battery + self.w_distance * normal_distance + self.w_memory * normal_memory
        return self.effective_deadline

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

    rospy.init_node("battery_charge_scheduler")
    rospy.Subscriber("/apriltag_box/real_odometry_sensor/odometry", Odometry, apriltag_callback)

    ecef_home = lla_to_ecef(*home_gps)
    ecef_obj = lla_to_ecef(*object_gps)

    ned = ecef_to_ned(ecef_obj, ecef_home, home_gps[0], home_gps[1])  # result in meters

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

    