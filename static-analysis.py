import ansi2html
from ansi2html import Ansi2HTMLConverter
import subprocess
import os

# Chemin vers le répertoire contenant le code à analyser
#code_dir = input("Entrez le chemin vers le dossier du code source : ")
web_apps_dir = input("Donnez le chemin vers le dossier des applications web : ")

# Boucle sur les 50 applications Web dans le répertoire
for app_dir in os.listdir(web_apps_dir):
    # Vérifie que le chemin est bien un dossier
    if os.path.isdir(os.path.join(web_apps_dir, app_dir)):
        # Chemin complet de l'application Web
        app_path = os.path.join(web_apps_dir, app_dir)
        
        print("****************************************************")
        print(app_path)
        print("*****************************************************")
        
        filename = app_path +'/.semgrepignore'
        subprocess.run(['touch', filename])

        # Vérifier si le fichier .semgrepignore existe déjà
        # if subprocess.run(['test', '-f', filename]).returncode == 0:
        #     print("Le fichier .semgrepignore existe déjà dans le répertoire " + app_path)
        #     print('_______________________________________________________________________________\n\n')

        # else : 
        #     # Création du fichier .semgrepignore
        #     subprocess.run(['touch', filename])
        #     print(f'Le fichier .semgrepignore a été créé avec succès dans le repertoire ' + app_path)
        #     print('_______________________________________________________________________________\n\n')


        # Commande à exécuter pour lancer Semgrep sur l'application Web
        semgrep_command = "/home/h4ck3r/.local/bin/semgrep --config=auto --severity 'ERROR' --verbose --max-target-bytes '100 MB' "+app_path
        
        semgrep_output = subprocess.check_output(semgrep_command, shell=True)

        # Convertit les codes ANSI en HTML
        conv = Ansi2HTMLConverter()
        html_output = conv.convert(semgrep_output.decode('utf-8'))
        #html_output = ansi2html.converter(semgrep_output.decode('utf-8'))

        # Écrit les résultats dans un fichier de sortie
        with open("results_"+app_dir+".html", "w") as file:
            file.write(html_output)
