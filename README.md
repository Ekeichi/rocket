# Expérience Rocket Controller - CXSOM

Expérience d'apprentissage d'un contrôleur de fusée utilisant des cartes auto-organisatrices (Self-Organizing Maps) avec CXSOM.

## 🎯 Objectif

Apprendre la relation entre **Error** (erreur de position), **Velocity** (vitesse) et **Thrust** (poussée) à partir de données de contrôle de fusée.

Le système utilise 3 cartes auto-organisatrices (SOM) interconnectées qui apprennent la fonction : `(Error, Velocity) → Thrust`

## 📁 Structure du Projet

```
.
├── xsom.cpp                        # Code source principal (définition du réseau)
├── xsom                            # Exécutable compilé
├── makefile                        # Automatisation des tâches
├── data/
│   └── rocket-discrete-controller.dat  # Dataset (2601 échantillons)
│
├── build-rocket-dataset.py         # Chargement des données
├── show-rocket-predictions.py      # Visualisation des prédictions
├── show-weights-history.py         # Évolution des poids
├── show-samples.py                 # Visualisation des échantillons
│
├── train.dot                       # Graphe de calcul pour l'entraînement
├── check.dot                       # Graphe de calcul pour la vérification
├── predict.dot                     # Graphe de calcul pour la prédiction
│
└── README.md                       # Ce fichier
```

## 🔧 Prérequis

- **CXSOM** installé (`cxsom-builder`, `cxsom-processor`)
- **Python 3** avec : `numpy`, `matplotlib`, `pycxsom`
- Fichier de données : `data/rocket-discrete-controller.dat` (2601 échantillons)

## 🚀 Démarrage Rapide

### 1. Compilation (si nécessaire)

```bash
make xsom
```

### 2. Configuration et lancement du processeur

```bash
make cxsom-set-config ROOT_DIR=./root-dir VENV=../cxsom-venv HOSTNAME=localhost PORT=10000 SKEDNET_PORT=20000 NB_THREADS=4
make cxsom-launch-processor
```

### 3. Préparation des données

```bash
make inputs-setup
```

### 4. Entraînement

```bash
make train-setup SAVE_PERIOD=1000 DATA_SIZE=2601 MAP_SIZE=500
make feed-train-inputs WALLTIME=30000
```

### 5. Visualiser l'entraînement

```bash
make show-weights-history
```

### 6. Vérification

```bash
make cxsom-clear-processor
make clear-checks
make cxsom-launch-processor
make check WEIGHTS_AT=30000 DATA_SIZE=2601 MAP_SIZE=500
make show-checks
```

### 7. Prédiction

```bash
make cxsom-clear-processor
make clear-predictions
make cxsom-launch-processor
make predict WEIGHTS_AT=30000 DATA_SIZE=2601 MAP_SIZE=500
make show-predictions
```

## 📖 Documentation Complète

Pour une procédure détaillée avec toutes les options et explications, consultez :

👉 **[PROCEDURE_LANCEMENT.md](PROCEDURE_LANCEMENT.md)**

## 🛠️ Commandes Utiles

```bash
make help                    # Liste toutes les commandes disponibles
make cxsom-help              # Commandes CXSOM
make cxsom-scan-vars         # Scanner les variables
python3 analyze_data.py      # Analyser les données brutes
python3 check-brain.py root-dir  # Vérifier l'état du cerveau
```

## 🔄 Réinitialisation Complète (Redémarrer de Zéro)

Pour tout nettoyer et redémarrer l'expérience complètement :

```bash
# 1. Arrêter le processeur
make cxsom-kill-processor

# 2. Nettoyer TOUTES les données
make clear-training
make clear-checks
make clear-predictions
make clear-saved-weights
make clear-samples

# 3. Option : Nettoyer complètement le root-dir
rm -rf root-dir/

# 4. Recompiler (si vous avez modifié le code)
make xsom

# 5. Redémarrer de zéro
make cxsom-launch-processor
make inputs-setup
make train-setup SAVE_PERIOD=1000 DATA_SIZE=2601 MAP_SIZE=500
make feed-train-inputs WALLTIME=30000
```

## 🧹 Nettoyage Partiel

Pour nettoyer seulement certaines parties :

```bash
make cxsom-kill-processor    # Arrêter le processeur
make clear-training          # Nettoyer l'entraînement seulement
make clear-checks            # Nettoyer les vérifications seulement
make clear-predictions       # Nettoyer les prédictions seulement
make clear-saved-weights     # ⚠️ Supprimer tous les poids sauvegardés
make clear-samples           # Nettoyer les échantillons d'entrée
```

## 📊 Fichiers de Sortie

- `root-dir/` : Toutes les variables et poids CXSOM
- Graphiques générés par les scripts `show-*.py`

## 🔗 Références

- Code source : [xsom.cpp](xsom.cpp)
- Makefile : [makefile](makefile)
- Documentation CXSOM : https://github.com/HerveFrezza-Buet/cxsom

## 📝 Notes

- Le dataset contient **2601 échantillons** de triplets `(Error, Velocity, Thrust)`
- L'entraînement se fait sur **30 000 itérations** par défaut (ajustable avec `WALLTIME`)
- Les poids sont sauvegardés toutes les **1000 itérations** (ajustable avec `SAVE_PERIOD`)
- La taille de chaque carte SOM est de **500 neurones** (ajustable avec `MAP_SIZE`)
