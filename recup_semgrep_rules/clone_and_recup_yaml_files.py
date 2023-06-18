import os
import git
import shutil
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
import time

def clone_et_copier():
    # Demander à l'utilisateur l'URL du dépôt
    url_depot = input("Entrez l'URL du dépôt : ")
    
    # Utiliser tkinter pour demander à l'utilisateur le dossier de clonage
    root = tk.Tk()
    root.withdraw()
    chemin_clonage = filedialog.askdirectory(title="Choisissez le dossier de clonage")

    # Simuler une barre de progression
    print("Clonage du dépôt en cours...")
    for i in tqdm(range(100)):
        time.sleep(0.01)  # remplacer ceci par votre opération réelle

    # Cloner le dépôt
    repo = git.Repo.clone_from(url_depot, chemin_clonage)
    print(f'Le dépôt a été cloné dans {chemin_clonage}.')

    # Utiliser tkinter pour demander à l'utilisateur le dossier de destination
    dossier_destination = filedialog.askdirectory(title="Choisissez le dossier de destination des fichiers .yaml")

    # Parcourir chaque dossier et sous-dossier
    for root, dirs, files in os.walk(chemin_clonage):
        for file in files:
            # Si le fichier est un fichier yaml
            if file.endswith('.yaml'):
                # Construire le chemin complet vers le fichier
                fichier_source = os.path.join(root, file)
                # Construire le chemin complet vers le dossier de destination
                fichier_destination = os.path.join(dossier_destination, file)
                # Vérifier si le fichier existe déjà dans le dossier de destination
                if not os.path.exists(fichier_destination):
                    # Copier le fichier vers le dossier de destination
                    shutil.copyfile(fichier_source, fichier_destination)
                    print(f'Le fichier {file} a été copié dans le dossier {dossier_destination}.')
                else:
                    print(f'Le fichier {file} existe déjà dans le dossier {dossier_destination}, il n\'a pas été copié.')

# Appeler la fonction
clone_et_copier()
