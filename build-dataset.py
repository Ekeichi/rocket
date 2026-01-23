import sys
import pycxsom as cx
import numpy as np

if len(sys.argv) < 2:
    print(f'Usage : {sys.argv[0]} <root-dir>')
    sys.exit(0)

root_dir = sys.argv[1]

# 1. Chargement des données
data = np.loadtxt('rocket-discrete-controller.dat') 

# Extraction des colonnes (Error, Speed, Thrust)
raw_error  = data[:, 0] # Col 1
raw_speed  = data[:, 1] # Col 2
raw_thrust = data[:, 2] # Col 3

# 2. Normalisation [0, 1] (CRUCIAL pour xsom)
# On garde les min/max pour pouvoir dé-normaliser plus tard si besoin
def normalize(arr):
    mi, ma = arr.min(), arr.max()
    return (arr - mi) / (ma - mi) if ma > mi else arr

data_error  = normalize(raw_error)
data_speed  = normalize(raw_speed)
# Pour le thrust (0 ou 15), la normalisation va donner 0 ou 1.
data_thrust = normalize(raw_thrust) 

nb_samples = len(data)
print(f"Nombre d'échantillons : {nb_samples}")

# 3. Envoi vers CXSOM
# On crée 3 "variables" statiques qui contiennent tout le dataset
# La syntaxe cxsom requiert la taille dans le type : "Map1D<Scalar>=SIZE"
type_str = f'Map1D<Scalar>={nb_samples}'

with cx.variable.Realize(cx.variable.path_from(root_dir, 'static', 'dataset_error'), cx.typing.make(type_str), 1, nb_samples) as v:
    v[0] = data_error

with cx.variable.Realize(cx.variable.path_from(root_dir, 'static', 'dataset_speed'), cx.typing.make(type_str), 1, nb_samples) as v:
    v[0] = data_speed

with cx.variable.Realize(cx.variable.path_from(root_dir, 'static', 'dataset_thrust'), cx.typing.make(type_str), 1, nb_samples) as v:
    v[0] = data_thrust