#!/usr/bin/env python

import rospy
from apriltag_ros.msg import AprilTagDetectionArray
from geometry_msgs.msg import Vector3
from collections import deque
import numpy as np

class TagVelocityEstimator:

    def __init__(self):
        self.prev_pose = None
        self.prev_time = None
        self.velocities_x = deque(maxlen=10)
        self.velocities_y = deque(maxlen=10)
        self.velocities_z = deque(maxlen=10)

        self.subscriber = rospy.Subscriber("/tag_detections", AprilTagDetectionArray, self.callback)
        self.velocity_pub = rospy.Publisher('/set_xyz_waypoint_speed', Vector3, queue_size=10)

    def callback(self, data):
        # Assuming you're interested in the first detection.
        # If you're interested in a specific tag ID, you'll need additional logic.
        if not data.detections:
            return

        detection = data.detections[0]
        current_pose = detection.pose.pose.pose.position
        current_time = detection.pose.header.stamp

        if self.prev_pose and self.prev_time:
            dt = (current_time - self.prev_time).to_sec()

            if dt > 0:  # Avoid division by zero
                dx = current_pose.x - self.prev_pose.x
                dy = current_pose.y - self.prev_pose.y
                dz = current_pose.z - self.prev_pose.z

                velocity_x = dx / dt
                velocity_y = dy / dt
                velocity_z = dz / dt

                self.velocities_x.append(velocity_x)
                self.velocities_y.append(velocity_y)
                self.velocities_z.append(velocity_z)

                avg_velocity_x = np.mean(self.velocities_x)
                avg_velocity_y = np.mean(self.velocities_y)
                avg_velocity_z = np.mean(self.velocities_z)
                rospy.loginfo("Average velocities (X, Y, Z): %s, %s, %s", avg_velocity_x, avg_velocity_y, avg_velocity_z)

                velocity_msg = Vector3()
                velocity_msg.x = avg_velocity_x
                velocity_msg.y = avg_velocity_y
                velocity_msg.z = avg_velocity_z
                self.velocity_pub.publish(velocity_msg)

        self.prev_pose = current_pose
        self.prev_time = current_time

if __name__ == '__main__':
    rospy.init_node('tag_velocity_estimator', anonymous=True)
    estimator = TagVelocityEstimator()
    rospy.spin()