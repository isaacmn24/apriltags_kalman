#!/usr/bin/env python

import rospy
import tf2_ros
import tf.transformations as tft
import tf2_geometry_msgs
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped, Pose
from nav_msgs.msg import Odometry
import math
import numpy as np
import pickle

def euclidean_distance(position):
    """Calculate Euclidean distance from the origin."""
    return math.sqrt(position.x**2 + position.y**2 + position.z**2)

class Simulador():
    def __init__(self):
        self.drone_odom     = PoseStamped()
        self.apriltag_odom  = PoseStamped()
        self.drone_frame    = "hummingbird/real_odometry_sensor"
        self.apriltag_frame = "apriltag_box/real_odometry_sensor"
        self.camera_frame   = "hummingbird/camera_link_optical"

        self.tf_buffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tf_buffer)

        self.pose_pub       = rospy.Publisher("/hummingbird/command/pose", PoseStamped, queue_size=10)
        self.pose_sub       = rospy.Subscriber("/hummingbird/real_odometry_sensor/odometry", Odometry, self.pose_callback)
        self.apriltag_sub   = rospy.Subscriber("/apriltag_box/real_odometry_sensor/odometry", Odometry, self.apriltag_callback)

        self.goal_coordinates = (0,0,0,0,0,0)

        return

    def pose_callback(self, msg):
        self.drone_odom.pose   = msg.pose.pose
        self.drone_odom.header = msg.header
        return

    def apriltag_callback(self, msg):
        self.apriltag_odom.pose   = msg.pose.pose
        self.apriltag_odom.header = msg.header
        return
    
    def get_transform_matrix(self, target_frame, source_frame, debugging=False):
        try:
            transformation = self.tf_buffer.lookup_transform(target_frame, source_frame, rospy.Time())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            rospy.logwarn(f"Transform lookup failed: {e}")
            return

        # Extract translation and rotation
        trans = transformation.transform.translation
        rot = transformation.transform.rotation

        # Convert quaternion to 4x4 rotation matrix
        quat = [rot.x, rot.y, rot.z, rot.w]
        matrix = tft.quaternion_matrix(quat)

        # Set translation in the matrix
        matrix[0, 3] = trans.x
        matrix[1, 3] = trans.y
        matrix[2, 3] = trans.z

        print(transformation)

        if debugging:
            print(f'\nTRANSFORM WITH TARGET: {target_frame} AND SOURCE: {source_frame}\n{transformation}\n\n{matrix}')

        return matrix
    
    def apply_transform(self, transform, pose, debugging=False):
        pos = pose.pose.position
        ori = pose.pose.orientation

        new_pose = np.array([
            pos.x - transform[0,3],
            pos.y - transform[1,3],
            pos.z - transform[2,3]
            ])

        # Convert quaternion to rotation matrix
        quat = [ori.x, ori.y, ori.z, ori.w]
        matrix = tft.quaternion_matrix(quat)  # 4x4 rotation matrix

        new_ori = np.dot(transform[0:3, 0:3], matrix[0:3, 0:3])
        new_ori_extended = np.identity(4)
        new_ori_extended[0:3, 0:3] = new_ori

        new_ori_quaternions = tft.quaternion_from_matrix(new_ori_extended)

        transformed_pose_matrix = np.identity(4)
        transformed_pose_matrix[0:3,0:3] = new_ori
        transformed_pose_matrix[0:3,3]   = new_pose

        transformed_pose = PoseStamped()
        transformed_pose.header = pose.header
        transformed_pose.pose.position.x    = new_pose[0]
        transformed_pose.pose.position.y    = new_pose[1]
        transformed_pose.pose.position.z    = new_pose[2]
        transformed_pose.pose.orientation.x = new_ori_quaternions[0]
        transformed_pose.pose.orientation.y = new_ori_quaternions[1]
        transformed_pose.pose.orientation.z = new_ori_quaternions[2]
        transformed_pose.pose.orientation.w = new_ori_quaternions[3]

        if debugging:
            print(f'\nTRANSFORM:\n{transform}\n\nOLD POSE:\n{pose}\n\nTRANSFORMED POSE:\n{transformed_pose}')

        return transformed_pose
    
    def calculate_desired_camera_pose(self, debugging=False):
        pose = self.apriltag_odom.pose

        # 1. Position
        x = pose.position.x
        y = pose.position.y
        z = pose.position.z

        x_desired = self.goal_coordinates[0]
        y_desired = self.goal_coordinates[1]
        z_desired = self.goal_coordinates[2]

        # 2. Orientation as quaternion
        q = pose.orientation
        quaternion = [q.x, q.y, q.z, q.w]

        roll_desired  = self.goal_coordinates[3]
        pitch_desired = self.goal_coordinates[4]
        yaw_desired   = self.goal_coordinates[5]
        q_desired = tft.quaternion_from_euler(roll_desired, pitch_desired, yaw_desired)
    
        # 3. Get desired pose quaternions
        x_goal = x - x_desired
        y_goal = y - y_desired
        z_goal = z - z_desired

        # Invert q
        q_inv = tft.quaternion_inverse(quaternion)

        # Multiply quaternions: q_desired * q⁻¹
        q_goal = tft.quaternion_multiply(q_inv, q_desired)

        print(q_goal)

        new_msg = PoseStamped()
        new_msg.header = self.apriltag_odom.header
        new_msg.pose.position.x = x_goal
        new_msg.pose.position.y = y_goal
        new_msg.pose.position.z = z_goal
        new_msg.pose.orientation.x = q_goal[0]
        new_msg.pose.orientation.y = q_goal[1]
        new_msg.pose.orientation.z = q_goal[2]
        new_msg.pose.orientation.w = q_goal[3]

        if debugging:
            print(f'\n\nAPRILTAG POSE:\n{pose}\n\nGOAL COORDINATES:\n{self.goal_coordinates}\n\nDIFFERENCE GOAL AND APRILTAGBOX:\n{new_msg}')

        return new_msg

    def calculate_diference_camera_pose(self, desired_camera_pose, camera_pose, debugging=False):
        # desired_camera_pose: PoseStamped
        # camera_pose: matrix

        pose = desired_camera_pose.pose

        # 1. Position
        x_desired = pose.position.x
        y_desired = pose.position.y
        z_desired = pose.position.z

        x = camera_pose[0,3]
        y = camera_pose[1,3]
        z = camera_pose[2,3]

        # 2. Orientation as quaternion
        q_desired = pose.orientation
        quaternion_desired = [q_desired.x, q_desired.y, q_desired.z, q_desired.w]

        rotation_matrix = camera_pose[:3, :3]
        q = tft.quaternion_from_matrix(camera_pose)
    
        # 3. Get desired pose quaternions
        x_goal = x_desired - x
        y_goal = y_desired - y
        z_goal = z_desired - z

        # Invert q
        q_inv = tft.quaternion_inverse(q)       

        # Multiply quaternions: q_desired * q⁻¹
        q_goal = tft.quaternion_multiply(q_inv, quaternion_desired)

        new_msg = PoseStamped()
        new_msg.header = self.apriltag_odom.header
        new_msg.pose.position.x = x_goal
        new_msg.pose.position.y = y_goal
        new_msg.pose.position.z = z_goal
        new_msg.pose.orientation.x = q_goal[0]
        new_msg.pose.orientation.y = q_goal[1]
        new_msg.pose.orientation.z = q_goal[2]
        new_msg.pose.orientation.w = q_goal[3]

        if debugging:
            print(f'\n\DESIRED:\n{pose}\n\nACTUAL COORDINATES:\n{camera_pose}\n\nNEW POSE:\n{new_msg}')

        return new_msg

    def calculate_desired_pose(self):
        camera_goal_coordinates = PoseStamped()
        camera_goal_coordinates.header = self.apriltag_odom.header

        camera_goal_coordinates.pose.position.x = self.apriltag_odom.pose.position.x + self.goal_coordinates[0]
        camera_goal_coordinates.pose.position.y = self.apriltag_odom.pose.position.y + self.goal_coordinates[1]
        camera_goal_coordinates.pose.position.z = self.apriltag_odom.pose.position.z + self.goal_coordinates[2]

        q_source = self.apriltag_odom.pose.orientation
        quaternion_source = [q_source.x, q_source.y, q_source.z, q_source.w]

        differenceAngle = tft.quaternion_from_euler(
            self.goal_coordinates[3],
            self.goal_coordinates[4],
            self.goal_coordinates[5]
        )

        #rotation = source * differenceAngle
        rotation = tft.quaternion_multiply(quaternion_source, differenceAngle)
        
        camera_goal_coordinates.pose.orientation.x = rotation[0]
        camera_goal_coordinates.pose.orientation.y = rotation[1]
        camera_goal_coordinates.pose.orientation.z = rotation[2]
        camera_goal_coordinates.pose.orientation.w = rotation[3]

        return camera_goal_coordinates

    def move_drone(self):

        t_drone_camera = self.get_transform_matrix(self.drone_frame, self.camera_frame)
        # camera_pose = self.apply_transform(t_drone_camera, self.drone_odom)
        # print(f'\nCAMERA POSE:\n{camera_pose}')
        # desired_camera_pose = self.calculate_desired_camera_pose(debugging=0)
        # print(f"\nDESIRED CAMERA POSE:\n{desired_camera_pose}")
        # difference_camera_pose = self.calculate_diference_camera_pose(desired_camera_pose, camera_pose, debugging=0)
        # print(f"\nCAMERA GOAL:\n{difference_camera_pose}")

        # t_camera_drone = np.linalg.inv(t_drone_camera)
        # # print(t_drone_camera)
        # # print(t_camera_drone)
        # coordinates_to_go = self.apply_transform(t_camera_drone, difference_camera_pose, debugging=True)

        camera_coordinates = self.calculate_desired_pose()
        print(f"\nDESIRED CAMERA POSE:\n{camera_coordinates}")

        drone_coordinates = self.apply_transform(t_drone_camera, camera_coordinates, debugging=1)

        # print(f"\nDESIRED DRONE POSE:\n{drone_coordinates}")

        return
    
    def wait_for_pose(self, timeout=5):
        """Wait until drone_odom is filled or timeout (in seconds) expires."""
        start_time = rospy.Time.now()
        rate = rospy.Rate(10)  # 10 Hz

        while not rospy.is_shutdown():
            if self.drone_odom.header.stamp != rospy.Time():
                return True  # Pose received

            if (rospy.Time.now() - start_time).to_sec() > timeout:
                rospy.logwarn("Timeout waiting for odometry message!")
                return False

            rate.sleep()


if __name__ == '__main__':
    rospy.init_node("drone_simulation")

    with open("/home/isaac/Downloads/apriltags_kalman/ros_workspace/covariance_matrices.pkl", "rb") as f:
        covariance_matrices = pickle.load(f)

    rospy.sleep(1)

    sim = Simulador()

    for coordinates in covariance_matrices:
        if sim.wait_for_pose():
            sim.goal_coordinates = coordinates
            print(f'Coordinates to go:\n{coordinates}')
            sim.move_drone()
            rospy.sleep(60)
        else:
            rospy.logwarn("Skipping move_drone: no pose data received.")

        rospy.sleep(1)