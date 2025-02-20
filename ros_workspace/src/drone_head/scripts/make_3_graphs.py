import rosbag
import matplotlib.pyplot as plt
from geometry_msgs.msg import PointStamped

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

# Plot for X
plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(blimp_x, label='Blimp', color='blue')
plt.plot(drone_x, label='Drone', color='red')
plt.ylabel('X Position')
plt.legend()
plt.grid(True)

# Plot for Y
plt.subplot(3, 1, 2)
plt.plot(blimp_y, label='Blimp', color='blue')
plt.plot(drone_y, label='Drone', color='red')
plt.ylabel('Y Position')
plt.legend()
plt.grid(True)

# Plot for Z
plt.subplot(3, 1, 3)
plt.plot(blimp_z, label='Blimp', color='blue')
plt.plot(drone_z, label='Drone', color='red')
plt.ylabel('Z Position')
plt.xlabel('Time (or datapoints)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()