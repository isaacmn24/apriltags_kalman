import rosbag
from geometry_msgs.msg import PointStamped

bag_path = 'motion_in_y_3.bag'
bag = rosbag.Bag(bag_path)

blimp_positions = []
blimp_times = []

for topic, msg, t in bag.read_messages():
    if topic == '/blimp/location':
        point = msg.point
        blimp_positions.append(point)
        blimp_times.append(msg.header.stamp)

bag.close()

velocities = []

for i in range(1, len(blimp_positions)):
    delta_x = blimp_positions[i].x - blimp_positions[i-1].x
    delta_y = blimp_positions[i].y - blimp_positions[i-1].y
    delta_z = blimp_positions[i].z - blimp_positions[i-1].z
    
    delta_t = (blimp_times[i] - blimp_times[i-1]).to_sec()
    
    velocity_x = delta_x / delta_t
    velocity_y = delta_y / delta_t
    velocity_z = delta_z / delta_t
    
    velocities.append((velocity_x, velocity_y, velocity_z))

# Compute the average velocity
average_velocity_x = sum([v[0] for v in velocities]) / len(velocities)
average_velocity_y = sum([v[1] for v in velocities]) / len(velocities)
average_velocity_z = sum([v[2] for v in velocities]) / len(velocities)

print(f"Average Velocity:")
print(f"Vx: {average_velocity_x:.2f} m/s, Vy: {average_velocity_y:.2f} m/s, Vz: {average_velocity_z:.2f} m/s")