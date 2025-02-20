#!/usr/bin/env python3

import rospy
import os
from gazebo_msgs.srv import SpawnModel, DeleteModel
from gazebo_msgs.msg import ModelState, ModelStates
from geometry_msgs.msg import Pose, Point, Quaternion, Twist

class ModelSpawnerMover:
    def __init__(self):
        rospy.init_node('model_spawner_mover')

        self.model_name = rospy.get_param('~model_name', 'simple_model')

        script_directory = os.path.dirname(os.path.realpath(__file__))
        self.model_path = rospy.get_param('~model_path', os.path.join(script_directory, '..', 'models', 'AprilTagBox', 'urdf_model.urdf'))  # Provide path to your URDF here
        self.move_speed = rospy.get_param('~move_speed', 0.1)

        rospy.wait_for_service('gazebo/spawn_urdf_model')
        self.spawn_srv = rospy.ServiceProxy('gazebo/spawn_urdf_model', SpawnModel)
        self.delete_srv = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)
        
        self.pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=10)

        self.spawn_model()
        rospy.sleep(1)  # Wait a bit for the model to be spawned
        self.move_model()

    def spawn_model(self):
        try:
            with open(self.model_path, 'r') as f:
                model_xml = f.read()

            pose = Pose(position=Point(x=5, y=5, z=10), orientation=Quaternion(x=0, y=0, z=0, w=1))
            self.spawn_srv(self.model_name, model_xml, "", pose, "world")

        except Exception as e:
            rospy.logerr("Error in spawning model: %s", str(e))

    def move_model(self):
        rate = rospy.Rate(10)
        model_state = ModelState()
        model_state.model_name = self.model_name
        model_state.pose = Pose(Point(x=5, y=5, z=10), Quaternion(x=0, y=0, z=0, w=1))
        model_state.twist = Twist()
        model_state.twist.linear.x = self.move_speed

        while not rospy.is_shutdown():
            self.pub.publish(model_state)
            model_state.pose.position.x += model_state.twist.linear.x * 0.1  # Assuming rate is 10Hz
            rate.sleep()

if __name__ == '__main__':
    try:
        ModelSpawnerMover()
    except rospy.ROSInterruptException:
        pass
