import sys
import pycxsom as cx
import numpy as np
import os

"""
This opens rocket-discrete-controller.dat and "copies" it into cxsom variables (img/error_data, img/velocity_data, img/thrust_data).
The data is normalized to [0, 1].
"""

if len(sys.argv) < 2:
    print(f'Usage : {sys.argv[0]} <root-dir>')
    sys.exit(0)

root_dir = sys.argv[1]
data_path = os.path.join(os.path.dirname(__file__), 'data', 'rocket-discrete-controller.dat')

if not os.path.exists(data_path):
    print(f"Error: Data file not found at {data_path}")
    sys.exit(1)

# Load data
try:
    data = np.loadtxt(data_path)
except Exception as e:
    print(f"Error loading data: {e}")
    sys.exit(1)

# 0: Error, 1: Velocity, 2: Thrust
raw_error = data[:, 0]
raw_velocity = data[:, 1]
raw_thrust = data[:, 2]

# Normalize Error and Velocity: [-98.0392, 98.0392] -> [0, 1]
# We use the observed min/max to fill the whole space [0,1]
error = (raw_error - raw_error.min()) / (raw_error.max() - raw_error.min())
velocity = (raw_velocity - raw_velocity.min()) / (raw_velocity.max() - raw_velocity.min())

# Normalize Thrust: {0, 15} -> {0, 1}
thrust = raw_thrust / 15.0

print(f"Data Loaded. Shape: {data.shape}")
print(f"Error Range: [{error.min()}, {error.max()}]")
print(f"Velocity Range: [{velocity.min()}, {velocity.max()}]")
print(f"Thrust Range: [{thrust.min()}, {thrust.max()}]")

# Randomize the dataset
indices = np.arange(len(data))
np.random.shuffle(indices)
error = error[indices]
velocity = velocity[indices]
thrust = thrust[indices]
print("Dataset randomized (shuffled).")

with cx.variable.Realize(cx.variable.path_from(root_dir, 'img', 'error_data')) as v_error:
    v_error[0] = error

with cx.variable.Realize(cx.variable.path_from(root_dir, 'img', 'velocity_data')) as v_velocity:
    v_velocity[0] = velocity

with cx.variable.Realize(cx.variable.path_from(root_dir, 'img', 'thrust_data')) as v_thrust:
    v_thrust[0] = thrust

print("cxsom variables written.")
