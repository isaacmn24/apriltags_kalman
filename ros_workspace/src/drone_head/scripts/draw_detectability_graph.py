import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

angles = np.linspace(0, 360, 1000)

# First function: 0 at 0 degrees, max at 90 degrees, and 0 at 180 degrees
max_distance = 13.5
distance_detectability1 = max_distance * np.sin(np.deg2rad(angles))

# Second function: 0 at 90 degrees, max at 180 degrees, and 0 at 270 degrees
distance_detectability2 = max_distance * np.sin(np.deg2rad(angles - 90))

distance_detectability3 = max_distance * np.sin(np.deg2rad(angles - 180))

distance_detectability4 = max_distance * np.sin(np.deg2rad(angles - 270))

# Getting the maximum of the two functions
max_distance_detectability = np.maximum(np.maximum(np.maximum(distance_detectability1, distance_detectability2), distance_detectability3), distance_detectability4)

# Plotting the graph of the maximum
plt.plot(angles, max_distance_detectability, label='Max Distance Detectability')
plt.xlabel('Angle (degrees)')
plt.ylabel('Max Distance Detectability (meters)')
plt.title('Four Tags')
plt.xlim([0, 400])
plt.ylim([0, 20])
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()