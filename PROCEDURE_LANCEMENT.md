# Procédure de Lancement - Expérience Rocket Controller

Cette procédure détaille les étapes pour lancer l'expérience d'apprentissage du contrôleur de fusée avec CXSOM.

## Vue d'ensemble

L'expérience apprend la relation entre **Error** (erreur de position), **Velocity** (vitesse) et **Thrust** (poussée) à partir du fichier de données `data/rocket-discrete-controller.dat`.

Le système utilise 3 cartes auto-organisatrices (SOM) interconnectées qui apprennent la fonction : `(Error, Velocity) → Thrust`

---

## Prérequis

- CXSOM installé (`cxsom-builder`, `cxsom-processor`)
- Python 3 avec numpy, matplotlib
- Fichier de données : `data/rocket-discrete-controller.dat`
- Exécutable `xsom` compilé (voir section Compilation)

---

## Compilation

Si l'exécutable `xsom` n'existe pas ou si vous avez modifié `xsom.cpp` :

```bash
make xsom
```

Ou manuellement :

```bash
g++ -o xsom `pkg-config --cflags cxsom-builder` xsom.cpp `pkg-config --libs cxsom-builder`
```

---

## Étape 1 : Configuration initiale

### 1.1 Créer le répertoire de travail

Si ce n'est pas déjà fait :

```bash
mkdir -p root-dir
```

### 1.2 Configurer CXSOM

```bash
make cxsom-set-config ROOT_DIR=./root-dir VENV=../cxsom-venv HOSTNAME=localhost PORT=10000 SKEDNET_PORT=20000 NB_THREADS=4
```

> **Note** : Adaptez `VENV` au chemin de votre environnement virtuel CXSOM.

### 1.3 Lancer le processeur

```bash
make cxsom-launch-processor
```

### 1.4 Vérifier l'état

```bash
make cxsom-scan-vars
```

---

## Étape 2 : Calibration (Optionnel)

Cette étape permet de visualiser les courbes d'apprentissage avec les paramètres définis dans `xsom.cpp`.

```bash
make clear-calibration
make cxsom-clear-processor
make calibration-setup GRID_SIDE=100
make calibrate
make show-calibration
```

---

## Étape 3 : Préparation des données d'entrée

### 3.1 Configuration des inputs

Cette étape charge les données depuis `data/rocket-discrete-controller.dat` (2601 échantillons) :

```bash
make inputs-setup
```

> Cette commande :
> - Envoie les règles d'input au processeur
> - Exécute `build-rocket-dataset.py` pour charger les données
> - Crée les variables : `img/error_data`, `img/velocity_data`, `img/thrust_data`

### 3.2 Vérifier les échantillons (Optionnel)

```bash
make show-samples
```

---

## Étape 4 : Entraînement

### 4.1 Configuration de l'entraînement

```bash
make train-setup SAVE_PERIOD=1000 DATA_SIZE=2601
```

Paramètres :
- `SAVE_PERIOD=1000` : Sauvegarde les poids toutes les 1000 itérations
- `DATA_SIZE=2601` : Nombre d'échantillons dans le dataset

### 4.2 Lancer l'entraînement

```bash
make feed-train-inputs WALLTIME=30000
```

> `WALLTIME=30000` : Le réseau s'entraîne pendant 30 000 pas de temps.

### 4.3 Surveiller l'évolution

Une fois l'entraînement terminé, visualiser les poids pour vérifier la convergence :

```bash
make show-weights-history
make show-rgb-mapping
```

> **Astuce** : Si l'entraînement n'est pas satisfaisant, relancez avec un `WALLTIME` plus élevé sans nettoyer :

```bash
make feed-train-inputs WALLTIME=100000
```

### 4.4 Nettoyer l'entraînement (après validation)

⚠️ **Attention** : Cette commande supprime les variables d'entraînement. Ne la lancez que si vous êtes satisfait :

```bash
make cxsom-clear-processor
make clear-training
```

---

## Étape 5 : Vérification (Check)

Cette étape vérifie que les cartes ont bien appris les triplets `(Error, Velocity, Thrust)`.

### 5.1 Visualiser les règles de vérification (Optionnel)

```bash
make show-check-rules
```

### 5.2 Lancer la vérification

```bash
make cxsom-clear-processor
make clear-checks
make check WEIGHTS_AT=30000 DATA_SIZE=2601
```

Paramètres :
- `WEIGHTS_AT=30000` : Utilise les poids sauvegardés à l'itération 30000
- `DATA_SIZE=2601` : Taille du dataset

### 5.3 Afficher les résultats

```bash
make show-checks
```

---

## Étape 6 : Prédiction

Cette étape utilise le réseau entraîné pour prédire la poussée (`Thrust`) à partir de `(Error, Velocity)`.

### 6.1 Visualiser les règles de prédiction (Optionnel)

```bash
make show-predict-rules
```

### 6.2 Lancer la prédiction

```bash
make cxsom-clear-processor
make clear-predictions
make predict WEIGHTS_AT=30000 DATA_SIZE=2601
```

### 6.3 Afficher les prédictions

```bash
make show-predictions
```

> Cette commande affiche les données d'entrée (`error_data`, `velocity_data`) et les prédictions de poussée (`predicted-thrust`).

---

## Étape 7 : Nettoyage complet

Pour repartir de zéro sur une nouvelle expérience :

```bash
make cxsom-kill-processor
make clear-calibration
make clear-samples
make clear-training
make clear-saved-weights  # ⚠️ Supprime tous les poids entraînés
make clear-checks
make clear-predictions
```

---

## Commandes utiles

### Voir toutes les commandes disponibles

```bash
make help
make cxsom-help
```

### Analyser les données brutes

```bash
python3 analyze_data.py
```

### Vérifier le cerveau (brain)

```bash
python3 check-brain.py <root-dir>
```

### Scanner les variables du processeur

```bash
make cxsom-scan-vars
```

### Redémarrer le processeur

```bash
make cxsom-kill-processor
make cxsom-launch-processor
```

---

## Workflow typique complet

Voici un enchaînement complet pour une expérience de A à Z :

```bash
# 1. Configuration initiale
make cxsom-set-config ROOT_DIR=./root-dir VENV=../cxsom-venv HOSTNAME=localhost PORT=10000 SKEDNET_PORT=20000 NB_THREADS=4
make cxsom-launch-processor

# 2. Préparation des inputs
make inputs-setup

# 3. Entraînement
make train-setup SAVE_PERIOD=1000 DATA_SIZE=2601
make feed-train-inputs WALLTIME=30000

# 4. Visualisation de l'entraînement
make show-weights-history

# 5. Vérification
make cxsom-clear-processor
make clear-checks
make cxsom-launch-processor
make check WEIGHTS_AT=30000 DATA_SIZE=2601
make show-checks

# 6. Prédiction
make cxsom-clear-processor
make clear-predictions
make cxsom-launch-processor
make predict WEIGHTS_AT=30000 DATA_SIZE=2601
make show-predictions
```

---

## Troubleshooting

### Le processeur ne démarre pas
```bash
make cxsom-kill-processor
make cxsom-launch-processor
```

### Erreur "FileNotFoundError" sur les données
Vérifiez que le fichier `data/rocket-discrete-controller.dat` existe.

### Les variables ne sont pas créées
```bash
make cxsom-scan-vars  # Pour voir l'état
make cxsom-ping-processor  # Pour vérifier que le processeur répond
```

### Le réseau ne converge pas
- Augmentez le `WALLTIME` : `make feed-train-inputs WALLTIME=100000`
- Vérifiez les paramètres dans `xsom.cpp` (alpha, sigma, etc.)
- Visualisez l'historique : `make show-weights-history`

---

## Références

- Code source : [`xsom.cpp`](xsom.cpp)
- Makefile : [`makefile`](makefile)
- Documentation CXSOM : https://github.com/HerveFrezza-Buet/cxsom
