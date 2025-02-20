import rosbag
import matplotlib.pyplot as plt
from geometry_msgs.msg import PointStamped
from mpl_toolkits import mplot3d

bag_path = 'motion_y_final_2.bag'
bag = rosbag.Bag(bag_path)

blimp_x = []
blimp_y = []
blimp_z = []

drone_x = []
drone_y = []
drone_z = []

for topic, msg, t in bag.read_messages():
    if topic == '/blimp/location':
        blimp_x.append(msg.point.x)
        blimp_y.append(msg.point.y)
        blimp_z.append(msg.point.z)
    elif topic == '/hummingbird/odometry_sensor1/position':
        drone_x.append(msg.point.x)
        drone_y.append(msg.point.y)
        drone_z.append(msg.point.z)

bag.close()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotting blimp in blue and drone in red
ax.plot(blimp_x, blimp_y, blimp_z, color='blue', label='Blimp')
ax.plot(drone_x, drone_y, drone_z, color='red', label='Drone')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')


ax.legend()

plt.show()