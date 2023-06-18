import os
import shutil
import tkinter as tk
from tkinter import filedialog

def chercher_et_copier():
    # Utiliser tkinter pour demander à l'utilisateur le dossier source
    root = tk.Tk()
    root.withdraw()
    dossier_source = filedialog.askdirectory(title="Choisissez le dossier source")

    # Utiliser tkinter pour demander à l'utilisateur le dossier de destination
    dossier_destination = filedialog.askdirectory(title="Choisissez le dossier de destination")

    # Parcourir chaque dossier et sous-dossier dans le dossier source
    for root, dirs, files in os.walk(dossier_source):
        for file in files:
            # Si le fichier est un fichier yaml
            if file.endswith('.yaml'):
                # Construire le chemin complet vers le fichier
                chemin_complet = os.path.join(root, file)

                # Ouvrir le fichier et lire son contenu
                with open(chemin_complet, 'r') as f:
                    contenu = f.read()

                # Si le mot 'Injection' est dans le contenu du fichier
                if 'Injection' in contenu:
                    # Construire le chemin complet vers le fichier de destination
                    fichier_destination = os.path.join(dossier_destination, file)

                    # Vérifier si le fichier existe déjà dans le dossier de destination
                    if not os.path.exists(fichier_destination):
                        # Copier le fichier vers le dossier de destination
                        shutil.copyfile(chemin_complet, fichier_destination)
                        print(f'Le fichier {file} a été copié dans le dossier {dossier_destination}.')
                    else:
                        print(f'Le fichier {file} existe déjà dans le dossier {dossier_destination}, il n\'a pas été copié.')

# Appeler la fonction
chercher_et_copier()
