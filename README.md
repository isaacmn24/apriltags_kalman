# apriltags_kalman

This repositaory contains the programs made for the Bachelor's Thesis titled **Autonomous Localization and Coordination of Tiny Aerial Robots relative to a LArger Aerial Platform** of the Mechatronics School from the Costa Rica Institute of Thecnology. The thesis was carried out within the [Flight Robotics and Perception Group (FRPG)]{https://www.aamirahmad.de/} from the University of Stuttgart, Germany. The thesis is available at THIS LINK (yet unavailable).

The sources and references, the license, and the specifics of the implementation can be read in the afore-mentioned thesis.

## Problem context

It is desired for the Parrot's ANAFI drones to locate themselves relative to a docking system using AprilTags and a Kalman Filter, and also to schedule their turn to go there. This is useful for autonomously recharing the drones in another aerial platform.

For this, a ROS environment is proposed with a Gazebo simulation and real-life tests to valide accuracy and even measure AprilTag detection' covariance.

## Repository overview

The solution comprises tests for a laboratory where a Vicon system is used as ground truth to compare the data with the AprilTag detection, and tests outside the laboratory where odometry and GPS localization is used instead.

Since different adaptations were needed for each of them, the repository is divided in two branches, one for laboratory tests and another for outside tests. In them, the specific usage of the developed programs is explained.



