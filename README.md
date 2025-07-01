# Tests inside Vicon room
In this branch, the ROS workspace and tests done inside the laboratory equipped with the Vicon system are found. Two experiments were performed: a covariance measurement experiment in three random locations and heihgts, and a validation experiment to measure the Kalman Filter error when including the covariance matrices previously calculated; the same positions were used here.

To use the implemented solutions, the workspace must be built. For this, inside the `ros_workspace` directory, the command `catkin_make` should be executed.

## Branch overview
In the ROS workspace, there are two main directories and two files of interest:

### Other files
Here a preset for rviz to better visualize the tests can be found as `rviz_config.rviz`. Also, there are two similar directories with tests:
- **covariance_tests** includes the CSV's with the measurements in all positions. The `ground_truth` files correspond to direct measurements with the Vicon system, whereas the `error` files correspond to the error between the ground truth tag position and the AprilTag's measured tag position. Furthermore, a python script named `statistics_analysis.py` creates another CSV with the statistical description of all positions of one of the two measurements.
- **inside_tests** has the same format of the measurements, but instead of the python script, it has a folder with the same name, which has three R scripts, one for a normality test of the error files, another for an ANOVA test, and a last one for a statistical hypothesis test.

### src
This contains all the ROS packages used. The custom ones are the following:
- **coordination_algorithm:** Contains the simulation 

