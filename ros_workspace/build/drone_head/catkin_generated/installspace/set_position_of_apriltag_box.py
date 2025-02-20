#!/usr/bin/env python3

import rospy
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from tf.transformations import quaternion_from_euler

def set_model_position():

    # Retrieve parameters from launch file
    model_name = rospy.get_param("~model_name", "apriltag_box")
    print("model_name =",model_name)
    x = rospy.get_param("~x", 0.0)
    y = rospy.get_param("~y", 0.0)
    z = rospy.get_param("~z", 0.0)
    roll = rospy.get_param("~roll", 0.0)
    pitch = rospy.get_param("~pitch", 0.0)
    yaw = rospy.get_param("~yaw", 0.0)

    rospy.wait_for_service('/gazebo/set_model_state')
    
    try:
        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        model_state = ModelState()
        model_state.model_name = model_name
        model_state.pose.position.x = x
        model_state.pose.position.y = y
        model_state.pose.position.z = z

        quat = quaternion_from_euler(roll, pitch, yaw)
        model_state.pose.orientation.x = quat[0]
        model_state.pose.orientation.y = quat[1]
        model_state.pose.orientation.z = quat[2]
        model_state.pose.orientation.w = quat[3]

        model_state.reference_frame = "world"

        response = set_state(model_state)
        if response.success:
            rospy.loginfo(f"Successfully moved {model_name} to ({x}, {y}, {z}) with orientation ({roll}, {pitch}, {yaw})")
        else:
            rospy.logwarn("Failed to move the model.")
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")

if __name__ == "__main__":
    # rospy.init_node('set_apriltag_box_position_node')
    rospy.init_node('set_apriltag_box_position_node', anonymous=True)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():

        set_model_position()
        rate.sleep()