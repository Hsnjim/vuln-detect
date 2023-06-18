import os
import tkinter as tk
from tkinter import filedialog

def choisir_dossier():
    root = tk.Tk()
    root.withdraw()
    dossier = filedialog.askdirectory(title="Choisissez le dossier source contenant les fichiers .yaml")
    return dossier

def choisir_fichier():
    root = tk.Tk()
    root.withdraw()
    fichier = filedialog.asksaveasfilename(defaultextension=".txt", title="Choisissez le fichier de destination pour sauvegarder les secondes lignes")
    return fichier

def extraire_ligne_yaml():
    dossier_source = choisir_dossier()
    fichier_destination = choisir_fichier()
    
    # Parcourir chaque dossier et sous-dossier
    for root, dirs, files in os.walk(dossier_source):
        for file in files:
            # Si le fichier est un fichier yaml
            if file.endswith('.yaml'):
                # Construire le chemin complet vers le fichier
                fichier_source = os.path.join(root, file)
                # Ouvrir le fichier yaml
                with open(fichier_source, 'r') as f:
                    lines = f.readlines()
                    # Si le fichier a au moins deux lignes
                    if len(lines) >= 2:
                        # Stocker la deuxième ligne dans le fichier de destination
                        with open(fichier_destination, 'a') as f_out:
                            f_out.write(lines[1])

# Utiliser la fonction
extraire_ligne_yaml()
