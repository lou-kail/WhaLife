"""
import os

fichier = open('data/txt/occurrence.txt', 'r', encoding='utf-8')
ligne = fichier.readline()
data = []
while ligne:
    data.append(ligne)
    ligne = fichier.readline()
fichier.close()
for i in range(len(data)):
    data[i] = data[i].strip()
    data[i] = data[i].replace('\t', '";"')
    data[i] = '"' + data[i] + '"\n'
os.makedirs("data/csv", exist_ok=True)
fichier = open('data/csv/occurence.csv', 'w', encoding='utf-8')
fichier.writelines(data)
fichier.close()
"""
import pandas as pd
import os

# Création du dossier de sortie si nécessaire
os.makedirs("data/csv", exist_ok=True)

# Lecture du fichier tabulé (sep='\t')
df = pd.read_csv('data/txt/occurrence.txt', sep='\t')

# Sauvegarde en CSV standard (séparateur virgule)
# index=False évite d'ajouter une colonne de numérotation
df.to_csv('data/csv/occurrence.csv', index=False, encoding='utf-8')