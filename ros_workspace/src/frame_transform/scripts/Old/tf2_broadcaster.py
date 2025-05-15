#!/usr/bin/env python3  

import rospy
import tf2_ros
import geometry_msgs.msg

def publish_transform(frame_id, child_frame_id, pose):
    br = tf2_ros.TransformBroadcaster()
    t = geometry_msgs.msg.TransformStamped()

    t.header.stamp = rospy.Time.now()
    t.header.frame_id = frame_id  # e.g., "world"
    t.child_frame_id = child_frame_id  # e.g., "drone_frame"
    t.transform.translation.x = pose.position.x
    t.transform.translation.y = pose.position.y
    t.transform.translation.z = pose.position.z
    t.transform.rotation = pose.orientation  # Assuming quaternion

    br.sendTransform(t)

def drone_odometry_callback(msg):
    """Callback for drone odometry updates"""
    publish_transform("world", "drone_frame", msg)

def apriltag_odometry_callback(msg):
    """Callback for object odometry updates"""
    publish_transform("world", "apriltag_frame", msg)

if __name__ == '__main__':
    rospy.init_node("tf_broadcaster")

    # Subscribe to odometry topics
    rospy.Subscriber("/hummingbird/real_odometry_sensor/pose", geometry_msgs.msg.Pose, drone_odometry_callback)
    rospy.Subscriber("/apriltag_box/real_odometry_sensor/pose", geometry_msgs.msg.Pose, apriltag_odometry_callback)

    rospy.spin()  # Keep the node running

