#!/usr/bin/env python3

import rospy
import os
import tf
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose, Point, Quaternion, PointStamped
from std_msgs.msg import Empty
from gazebo_msgs.msg import ModelState
from std_msgs.msg import Float64
from gazebo_msgs.srv import SetModelState

global move_flag
move_flag = 1

def change_move_flag(data):
    global move_flag
    move_flag=data.data

class SpawnAndMoveModel:
    initial_x = 5
    initial_y = 20  
    initial_z = 6.0  
    target_x = 25.0  
    step_size = 0.005
    def __init__(self):
        rospy.init_node('spawn_and_move_blimp')
        self.model_name = 'blimp_model' 
        self.spawn_model_service = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
   
        self.delete_model_service = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        self.pub = rospy.Publisher('/cmd_vel', Empty, queue_size=1)
        self.tf_listener = tf.TransformListener()

    def spawn_model(self):
        try:
            script_directory = os.path.dirname(os.path.realpath(__file__))
            model_file_path = os.path.join(script_directory, '..', 'models', 'AprilTagBox', 'model.sdf')  # Assuming model file is 'model.urdf'

            initial_pose = Pose(Point(SpawnAndMoveModel.initial_x, SpawnAndMoveModel.initial_y, SpawnAndMoveModel.initial_z), Quaternion(0, 0, -0.7071, 0.7071))  
            self.spawn_model_service(model_name=self.model_name,
                                        model_xml=open(model_file_path, 'r').read(),
                                        robot_namespace='blimp',
                                        initial_pose=initial_pose,
                                        reference_frame="world",
                                    )
        except rospy.ServiceException as e:
            rospy.logerr("Spawn service call failed: {0}".format(e))



    """ def spawn_model(self):
        try:
            #model_xml=open('/home/mahmoud/model_editor_models/AprilTagBox/model.sdf', 'r').read(),

            script_directory = os.path.dirname(os.path.realpath(__file__))

            # Build the relative path to the model file
            model_file_path = os.path.join(script_directory, '..', 'models', 'AprilTagBox', 'urdf_model.sdf')

            initial_pose = Pose(Point(10, 12, 5), Quaternion(0, 0, -0.7071, 0.7071))  
            self.spawn_model_service(model_name=self.model_name,
                                        model_xml=open(model_file_path, 'r').read(),
                                        robot_namespace='blimp',
                                        initial_pose=initial_pose,
                                        reference_frame="world"
                                    )
        except rospy.ServiceException as e:
            rospy.logerr("Spawn service call failed: {0}".format(e)) """

    def move_model(self):
        global move_flag
        rate = rospy.Rate(100)  
        forward = True
        
        set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        self.blimp_location_pub = rospy.Publisher('/blimp/location', PointStamped, queue_size=10)
        model_state = ModelState()

        my_model_name = self.model_name  

        

        x = 0

        model_state.model_name = my_model_name

        forward = False

        while not rospy.is_shutdown():
            if(move_flag ==  0):
                rospy.on_shutdown()
            try:
                
                if(forward):
                    x += SpawnAndMoveModel.step_size
                else:
                    x-=SpawnAndMoveModel.step_size
                if(x>SpawnAndMoveModel.target_x):
                    forward=False
                
                if(x<-SpawnAndMoveModel.target_x):
                    forward=True         

                model_state.pose.position.x = SpawnAndMoveModel.initial_x 
                model_state.pose.position.y = SpawnAndMoveModel.initial_y + x
                model_state.pose.position.z = SpawnAndMoveModel.initial_z 

                model_state.pose.orientation.x = 0
                model_state.pose.orientation.y = 0
                model_state.pose.orientation.z = -0.7071
                model_state.pose.orientation.w = 0.7071

                blimp_location = PointStamped()
                blimp_location.header.stamp = rospy.Time.now()
                blimp_location.header.frame_id = 'world'
                blimp_location.point = model_state.pose.position
                self.blimp_location_pub.publish(blimp_location)
                
                try:
                    set_model_state(model_state)
                    rospy.loginfo(f"Object moved to X: {model_state.pose.position.x}, Y: {model_state.pose.position.y}, Z: {model_state.pose.position.z}")
                except rospy.ServiceException as e:
                    rospy.logerr("Service call failed: %s" % e)

                rate.sleep()

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue

    def delete_model(self):
        try:
            self.delete_model_service(self.model_name)
        except rospy.ServiceException as e:
            rospy.logerr("Delete service call failed: {0}".format(e))

if __name__ == '__main__':
    try:
        rospy.sleep(5)

        rospy.wait_for_service('/gazebo/spawn_sdf_model')
       
        rospy.wait_for_service('/gazebo/delete_model')
        rospy.wait_for_service('/gazebo/set_model_state')
        sub=rospy.Subscriber('docking_done', Float64, callback=change_move_flag)
        model_spawner = SpawnAndMoveModel()

        
    
        model_spawner.spawn_model()
        rospy.sleep(1)  # Wait for the model to spawn
        model_spawner.move_model()
        rospy.spin()

    except rospy.ROSInterruptException:

        pass