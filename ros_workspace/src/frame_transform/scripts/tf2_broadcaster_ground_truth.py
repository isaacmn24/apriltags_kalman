#!/usr/bin/env python3  

import rospy
import tf2_ros
import geometry_msgs.msg
import tf_conversions
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from sensor_msgs.msg import NavSatFix
from uav_msgs.msg import uav_pose
import numpy as np
from pyproj import Proj
from pyproj.transformer import Transformer

home_gps = (48.750186, 9.105734, 514.354)   # (lat, lon, alt)
object_gps = (48.750231, 9.105686, 473)

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

class Broadcaster():
    def __init__(self):
        self.drone_pose_vicon           = geometry_msgs.msg.PoseStamped()
        self.drone_attitude_rpy         = geometry_msgs.msg.Vector3Stamped()
        self.marker_board_pose          = geometry_msgs.msg.PoseStamped()
        self.relative_gimbal_quaternion = np.zeros(4)
        self.tag_detection              = geometry_msgs.msg.PoseWithCovarianceStamped()
        self.br                         = tf2_ros.TransformBroadcaster()

        #Subscriber / Publishers
        self.marker_board_sub = rospy.Subscriber("/fc0/pose", uav_pose, self.marker_board_pose_callback)
        self.drone_pose_vicon_sub = rospy.Subscriber("/anafi/drone/gps/location", NavSatFix, self.drone_callback)
        self.camera_base_attitude_sub = rospy.Subscriber("/anafi/gimbal/relative", geometry_msgs.msg.Vector3Stamped, self.camera_attitude_callback)
        self.drone_attitude_sub = rospy.Subscriber("/anafi/drone/attitude", geometry_msgs.msg.QuaternionStamped, self.drone_attitude_callback)
        self.tag_detections_sub = rospy.Subscriber("/tag_detections_corrected", geometry_msgs.msg.PoseWithCovarianceStamped, self.apriltag_callback)

        return

    def publish_apriltag_box_frame(self):
        ecef_home = lla_to_ecef(*home_gps)
        ecef_obj = lla_to_ecef(*object_gps)

        ned = ecef_to_ned(ecef_obj, ecef_home, home_gps[0], home_gps[1])

        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = self.drone_pose_vicon.header.stamp
        t.header.frame_id = "world"
        t.child_frame_id = "marker_board_1"
        t.transform.translation.x = self.marker_board_pose.pose.position.x
        t.transform.translation.y = self.marker_board_pose.pose.position.y
        t.transform.translation.z = self.marker_board_pose.pose.position.z

        t.transform.rotation.x = self.marker_board_pose.pose.orientation.x
        t.transform.rotation.y = self.marker_board_pose.pose.orientation.y
        t.transform.rotation.z = self.marker_board_pose.pose.orientation.z
        t.transform.rotation.w = self.marker_board_pose.pose.orientation.w

        self.br.sendTransform(t)
        print("Marker board frame published")
        return

    def publish_anafi_pose_frame(self):
        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = self.drone_pose_vicon.header.stamp
        t.header.frame_id = "world"
        t.child_frame_id = "anafi_localization_1"
        t.transform.translation.x = self.drone_pose_vicon.pose.position.x
        t.transform.translation.y = self.drone_pose_vicon.pose.position.y
        t.transform.translation.z = self.drone_pose_vicon.pose.position.z

        q = self.drone_pose_vicon.pose.orientation
        q_array = [q.x, q.y, q.z, q.w]

        q_rotated = tf_conversions.transformations.quaternion_multiply([0,0,1,0], q_array)

        t.transform.rotation.x = q_rotated[0]
        t.transform.rotation.y = q_rotated[1]
        t.transform.rotation.z = q_rotated[2]
        t.transform.rotation.w = q_rotated[3]
        
        self.br.sendTransform(t)

        print("Anafi frame published")
        return

    def publish_rotated_anafi_pose_frame(self):
        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = self.drone_pose_vicon.header.stamp
        t.header.frame_id = "anafi_localization_1"
        t.child_frame_id = "anafi_rotated"
        t.transform.translation.x = self.drone_pose_vicon.pose.position.x
        t.transform.translation.y = self.drone_pose_vicon.pose.position.y
        t.transform.translation.z = self.drone_pose_vicon.pose.position.z

        t.transform.rotation.x = self.drone_pose_vicon.pose.orientation.x
        t.transform.rotation.y = self.drone_pose_vicon.pose.orientation.y
        t.transform.rotation.z = self.drone_pose_vicon.pose.orientation.z
        t.transform.rotation.w = self.drone_pose_vicon.pose.orientation.w
        
        self.br.sendTransform(t)

        print("Anafi frame published")
        return

    def publish_camera_frame(self):
        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = self.drone_pose_vicon.header.stamp
        # t.header.frame_id = "anafi_localization_combined"
        t.header.frame_id = "anafi_localization_1"
        t.child_frame_id = "camera_frame"
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.088
        t.transform.translation.z = 0.0

        # Rotate 90 deg around z axis because vicon system
        # t.transform.rotation.x = np.sqrt(2)/2
        # t.transform.rotation.w = -np.sqrt(2)/2

        t.transform.rotation.w = 1

        self.br.sendTransform(t)
        print("sent camera frame relative to anafi_localization_combined")
        return
    
    def publish_gimbaled_camera_frame(self):
        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = self.drone_pose_vicon.header.stamp
        t.header.frame_id = "anafi_localization_1"
        # t.header.frame_id = "anafi_localization_combined"
        t.child_frame_id = "gimbaled_camera_frame"

        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.088
        t.transform.translation.z = 0.0

        q_array = self.relative_gimbal_quaternion

        q_rotated = tf_conversions.transformations.quaternion_multiply([-0.707,0,0,0.707], q_array)

        t.transform.rotation.x = q_rotated[0]
        t.transform.rotation.y = q_rotated[1]
        t.transform.rotation.z = q_rotated[2]
        t.transform.rotation.w = q_rotated[3]

        self.br.sendTransform(t)
        print("sent gimbaled camera frame ")

    def publish_correct_camera_frame(self):
        """ This frame is rotated according to apriltag standard """
        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = self.drone_pose_vicon.header.stamp
        t.header.frame_id = "gimbaled_camera_frame"
        t.child_frame_id = "correct_camera_frame"
        
        # qZ = tf_conversions.transformations.quaternion_from_euler(0, 0, np.pi/2)  # (roll, pitch, yaw) = (0, 0, π/2)
        
        # #q_enu = self.relative_gimbal_quaternion

        # t.transform.rotation.x = qZ[0]
        # t.transform.rotation.y = qZ[1]
        # t.transform.rotation.z = qZ[2]
        # t.transform.rotation.w = qZ[3]

        t.transform.rotation.w = 1

        self.br.sendTransform(t)
        print("sent correct camera frame ")

        return

    def publish_tag_detection_frame(self):
        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = self.drone_pose_vicon.header.stamp
        t.header.frame_id = "correct_camera_frame"
        # t.header.frame_id = "anafi_localization_1"
        t.child_frame_id = "tag_frame"

        t.transform.translation.x = self.tag_detection.pose.pose.position.x
        t.transform.translation.y = self.tag_detection.pose.pose.position.y
        t.transform.translation.z = self.tag_detection.pose.pose.position.z

        t.transform.rotation = self.tag_detection.pose.pose.orientation
        # t.transform.rotation.w = 1
        
        self.br.sendTransform(t)
        print("sent tag detection frame ")
        return
    
    def publish_oriented_tag_detection_frame(self):
        """ This frame is rotated to match marker_board """
        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = self.drone_pose_vicon.header.stamp
        t.header.frame_id = "tag_frame_bad"
        t.child_frame_id = "tag_frame"
        
        q_tag = self.tag_detection.pose.pose.orientation
        quaternions_tag = [q_tag.x, q_tag.y, q_tag.z, q_tag.w]
        new_q = tf_conversions.transformations.quaternion_multiply([0,0,-0.707,0.707], quaternions_tag)

        t.transform.rotation.x = 0
        t.transform.rotation.y = 0.707
        t.transform.rotation.z = 0
        t.transform.rotation.w = 0.707

        self.br.sendTransform(t)
        print("sent correct camera frame ")

        return

    def marker_board_pose_callback(self,msg):
        self.marker_board_pose.header = msg.header
        self.marker_board_pose.pose.orientation = msg.orientation
        self.marker_board_pose.pose.position.x = ned[0]
        self.marker_board_pose.pose.position.y = ned[1]
        self.marker_board_pose.pose.position.z = ned[2]
        return

    def drone_attitude_callback(self,msg):
        self.drone_pose_vicon.pose.orientation = msg.quaternion

        self.marker_board_pose.header = msg.header
        self.marker_board_pose.pose.orientation.w = 1
        self.marker_board_pose.pose.position.x = ned[0]
        self.marker_board_pose.pose.position.y = ned[1]
        self.marker_board_pose.pose.position.z = ned[2]


        return
    
    def drone_callback(self,msg):
        """Callback for drone odometry updates"""
        ecef_drone = lla_to_ecef(msg.latitude, msg.longitude, msg.altitude)
        ned = ecef_to_ned(ecef_drone, ecef_home, home_gps[0], home_gps[1])  # result in meters

        self.drone_pose_vicon.header          = msg.header
        self.drone_pose_vicon.pose.position.x = ned[0]
        self.drone_pose_vicon.pose.position.y = ned[1]
        self.drone_pose_vicon.pose.position.z = ned[2]
        return

    def apriltag_callback(self,msg):
        """Callback for object odometry updates"""
        self.tag_detection = msg
        # self.publish_transform("camera_frame", "apriltag_frame", msg)

    def camera_attitude_callback(self,msg):
        """Callback for object odometry updates"""
        self.relative_gimbal_quaternion = quaternion_from_euler(msg.vector.x, msg.vector.y, msg.vector.z)

if __name__ == '__main__':
    rospy.init_node("tf_broadcaster")

    ecef_home = lla_to_ecef(*home_gps)
    ecef_obj = lla_to_ecef(*object_gps)

    ned = ecef_to_ned(ecef_obj, ecef_home, home_gps[0], home_gps[1])  # result in meters

    brc = Broadcaster()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        brc.publish_apriltag_box_frame()
        brc.publish_anafi_pose_frame()
        #brc.publish_camera_frame()
        brc.publish_gimbaled_camera_frame()
        brc.publish_correct_camera_frame()
        brc.publish_tag_detection_frame()
        #brc.publish_oriented_tag_detection_frame()
        rate.sleep()

