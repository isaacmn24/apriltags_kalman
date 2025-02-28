#!/usr/bin/env python

import rospy
import tf2_ros
import geometry_msgs.msg

def transform_pose(target_frame, source_frame):
    """Transforms a pose from the source_frame to the target_frame using TF2."""
    rospy.loginfo(f"Transforming pose from {source_frame} to {target_frame}...")

    # Create TF buffer and listener
    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)

    try:
        # Wait for the transform to be available
        tf_buffer.lookup_transform(target_frame, source_frame, rospy.Time(0), rospy.Duration(1.0))

        # Create an identity PoseStamped in source_frame
        pose = geometry_msgs.msg.PoseStamped()
        pose.header.frame_id = source_frame
        pose.header.stamp = rospy.Time.now()
        pose.pose.position.x = 0.0
        pose.pose.position.y = 0.0
        pose.pose.position.z = 0.0
        pose.pose.orientation.w = 1.0  # Identity quaternion

        # Transform pose to target_frame
        transformed_pose = tf_buffer.transform(pose, target_frame, rospy.Duration(1.0))
        return transformed_pose.pose

    except tf2_ros.LookupException as e:
        rospy.logwarn(f"Transform lookup failed: {e}")
        return None
    except tf2_ros.ExtrapolationException as e:
        rospy.logwarn(f"Transform extrapolation error: {e}")
        return None

if __name__ == '__main__':
    # Initialize ROS node
    rospy.init_node("tf_listener")

    # Example: Transform object's pose into drone's frame
    rospy.sleep(1)  # Give some time for TF to populate
    pose_in_drone_frame = transform_pose("drone_frame", "object_frame")

    if pose_in_drone_frame:
        rospy.loginfo(f"Object's pose in drone frame: {pose_in_drone_frame}")
    else:
        rospy.logwarn("Could not transform object pose to drone frame.")

    rospy.spin()
