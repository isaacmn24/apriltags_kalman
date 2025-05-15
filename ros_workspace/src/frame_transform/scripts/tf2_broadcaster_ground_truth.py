#!/usr/bin/env python3  

import rospy
import tf2_ros
import geometry_msgs.msg
import tf_conversions
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import numpy as np
from anafi_control.msg import State

class Broadcaster():
    def __init__(self):
        self.drone_state = State()
        self.drone_pose_vicon = geometry_msgs.msg.PoseStamped()
        self.relative_gimbal_rpy = geometry_msgs.msg.Vector3Stamped()
        self.drone_attitude = geometry_msgs.msg.QuaternionStamped()
        self.drone_attitude_rpy = geometry_msgs.msg.Vector3Stamped()
        self.relative_gimbal_quaternion = np.zeros(4)
        self.tag_detection = geometry_msgs.msg.PoseWithCovarianceStamped()
        self.br = tf2_ros.TransformBroadcaster()

        #Subscriber / Publishers
        self.drone_pose_vicon_sub = rospy.Subscriber("/vrpn_client_node/anafi_localization_1/pose", geometry_msgs.msg.PoseStamped, self.drone_callback)
        self.camera_base_attitude_sub = rospy.Subscriber("/anafi/gimbal/relative", geometry_msgs.msg.Vector3Stamped, self.camera_attitude_callback)
        self.drone_attitude_sub = rospy.Subscriber("/anafi/drone/attitude", geometry_msgs.msg.QuaternionStamped, self.drone_attitude_callback)
        self.tag_detections_sub = rospy.Subscriber("/tag_detections_corrected", geometry_msgs.msg.PoseWithCovarianceStamped, self.apriltag_callback)
        self.drone_state_sub = rospy.Subscriber("/anafi/position_control/state_enu", State, self.state_callback)
        self.drone_attitude_pub = rospy.Publisher("/anafi/drone/attitude_rpy",geometry_msgs.msg.Vector3Stamped,queue_size=1)

    def publish_combined_anafi_pose_frame(self):
        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = self.drone_pose_vicon.header.stamp
        t.header.frame_id = "world"
        t.child_frame_id = "anafi_localization_combined"
        t.transform.translation.x = self.drone_pose_vicon.pose.position.x
        t.transform.translation.y = self.drone_pose_vicon.pose.position.y
        t.transform.translation.z = self.drone_pose_vicon.pose.position.z

        t.transform.rotation.w = 1
        
        self.br.sendTransform(t)

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

    def drone_attitude_callback(self,msg):
        self.drone_attitude = msg.quaternion
        return
    
    def drone_callback(self,msg):
        """Callback for drone odometry updates"""
        self.drone_pose_vicon = msg    
        # r,p,y = np.rad2deg(euler_from_quaternion([msg.pose.orientation.x,msg.pose.orientation.y,msg.pose.orientation.z,msg.pose.orientation.w]))
        # print("roll, pitch, yaw",r,p,y)
        #self.publish_transform("world", "drone_frame", msg)

    def apriltag_callback(self,msg):
        """Callback for object odometry updates"""
        self.tag_detection = msg
        # self.publish_transform("camera_frame", "apriltag_frame", msg)

    def camera_attitude_callback(self,msg):
        """Callback for object odometry updates"""
        self.relative_gimbal_rpy = msg
        # q = quaternion_from_euler(msg.vector.x,msg.vector.y,msg.vector.z)
        # self.publish_transform("anafi_localization", "camera_frame", q)

        self.relative_gimbal_quaternion = quaternion_from_euler(msg.vector.x, msg.vector.y, msg.vector.z)

    def state_callback(self,msg):
        self.drone_state = msg
        return

if __name__ == '__main__':
    rospy.init_node("tf_broadcaster")

    brc = Broadcaster()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        brc.publish_combined_anafi_pose_frame()
        #brc.publish_camera_frame()
        brc.publish_gimbaled_camera_frame()
        brc.publish_correct_camera_frame()
        brc.publish_tag_detection_frame()
        #brc.publish_oriented_tag_detection_frame()
        rate.sleep()

