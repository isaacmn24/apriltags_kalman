import pickle
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Load the pickle file
with open("covariance_matrices.pkl", "rb") as f:
    data = pickle.load(f)

for i in data:
    print(f"{i}: {np.round(data[i],3)}\n\n")