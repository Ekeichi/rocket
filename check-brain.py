import sys
import pycxsom as cx
import os

if len(sys.argv) < 2:
    print(f'Usage : {sys.argv[0]} <root-dir>')
    sys.exit(0)

root_dir = sys.argv[1]
maps = ['Error', 'Velocity', 'Thrust']
weights = ['We-0', 'Wc-0'] # On vérifie externe et contextuel

print(f"--- ANALYSE DU CERVEAU (Dossier: {root_dir}) ---")
all_good = True
max_snapshots = 999999

for m in maps:
    for w in weights:
        # Attention au chemin: saved/MapName/WeightName
        full_name = f"{m}/{w}"
        path = cx.variable.path_from(root_dir, 'saved', full_name)
        
        # Vérification physique
        if not os.path.exists(path + '.var'):
            print(f"❌ MANQUANT : {full_name}")
            all_good = False
            continue
            
        # Vérification logique
        try:
            with cx.variable.Realize(path) as v:
                r = v.time_range()
                count = r[1]
                size_kb = os.path.getsize(path + '.var') / 1024
                
                status = "✅ OK" if count > 10 else "⚠️ VIDE"
                if count < 10: all_good = False
                
                # On garde le nombre minimal de snapshots commun à tous
                if count > 0: max_snapshots = min(max_snapshots, count)
                
                print(f"{status} | {full_name:<15} | Snapshots: {count:<4} | Taille: {size_kb:.1f} Ko | Type: {v.datatype}")
        except Exception as e:
            print(f"❌ ERREUR LECTURE : {full_name} ({e})")
            all_good = False

print("-" * 40)
if all_good:
    print(f"Conclusion : CERVEAU SAIN. Vous avez {max_snapshots} instantanés valides.")
    print(f"Recommandation : Utilisez WEIGHTS_AT={max_snapshots - 1}")
else:
    print("Conclusion : CERVEAU ENDOMMAGÉ (Fichiers manquants ou vides).")
    print("Action requise : Relancer l'entraînement (Step 4 de la procédure précédente).")