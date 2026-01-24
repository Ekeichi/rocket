import sys
import os
import numpy as np
import pycxsom as cx

def normalize(v):
    v_min, v_max = v.min(), v.max()
    if v_max - v_min == 0: return v
    return (v - v_min) / (v_max - v_min)

if len(sys.argv) < 2:
    print(f"Usage : {sys.argv[0]} <root-dir>")
    sys.exit(1)

root_dir = sys.argv[1]
data_file = "data/rocket-discrete-controller.dat"

if not os.path.exists(data_file):
    print(f"Error: {data_file} not found.")
    sys.exit(1)

# Chargement et préparation
raw_data = np.loadtxt(data_file)
np.random.shuffle(raw_data) # Important !

errors = normalize(raw_data[:, 0])
velocities = normalize(raw_data[:, 1])
thrusts = normalize(raw_data[:, 2])

nb_samples = len(raw_data)
print(f"Data Loaded. Shape: {raw_data.shape}")

# Écriture avec définition explicite pour création automatique si inexistant
type_str = f'Map1D<Scalar>={nb_samples}'

def write_var(name, data):
    path = cx.variable.path_from(root_dir, 'img', name)
    # On spécifie le type, cache_size et file_size pour permettre la création
    with cx.variable.Realize(path, cx.typing.make(type_str), 1, nb_samples) as v:
        v[0] = data
        print(f"Written {name}")

write_var('error_data', errors)
write_var('velocity_data', velocities)
write_var('thrust_data', thrusts)