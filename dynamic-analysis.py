import os
import time
import subprocess
from zapv2 import ZAPv2
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import Tk

def demander_chemin_fichier(prompt, choisir_dossier=False):
    root = Tk()
    root.withdraw()
    if choisir_dossier:
        fichier_chemin = filedialog.askdirectory(title=prompt)
    else:
        fichier_chemin = filedialog.askopenfilename(title=prompt)
    return fichier_chemin

# Demander à l'utilisateur les informations nécessaires
urls_file_path = demander_chemin_fichier("Veuillez sélectionner le fichier contenant les URL (ex: urls.txt) : ")
api_key = input("Veuillez entrer la clé API de ZAP : ")
reports_folder = demander_chemin_fichier("Veuillez sélectionner le dossier où stocker les rapports générés (ex: rapports) : ", choisir_dossier=True)
graphs_folder = demander_chemin_fichier("Veuillez sélectionner le dossier où stocker les images des graphiques générés (ex: graphiques) : ", choisir_dossier=True)

# Lire les URL d'applications à scanner à partir du fichier texte
with open(urls_file_path, "r") as f:
    apps = [url.strip() for url in f.readlines()]

# Port utilisé par ZAP
zap_port = 8080

def scan_app(zap, app_url):                                                                        
    zap.urlopen(app_url)                                                                           
    time.sleep(10)                                                                                  

    print("Spidering starting .....")                                                                                           
    spider_id = zap.spider.scan(url=app_url, apikey=api_key) 
    time.sleep(5)                                     
    while int(zap.spider.status(spider_id)) < 100:   
        print("Pourcentage d'execution du spidering " + zap.spider.status(spider_id) + "%")                                                                                                                                                
        time.sleep(2)                                                                              
    print("Spider completed.")

    print("Active scan starting .....")
    ascan_id = zap.ascan.scan(url=app_url, apikey=api_key)
    while int(zap.ascan.status(ascan_id)) < 100:
        print("Pourcentage d'execution du ascan " + zap.ascan.status(ascan_id) + "%")         
        time.sleep(2)
    print("Ascan completed")

def generate_report(zap, app_url):
    print("Génération de rapport en cours ....")
    report_file = "{}/{}_report.html".format(reports_folder, app_url.replace("://", "_").replace("/", "_"))
    with open(report_file, "wb") as f:
        f.write(zap.core.htmlreport(api_key).encode('utf-8'))
    print("Rapport généré")
        

def plot_alerts_by_risk(zap, app_url):
    print("Génération du graphe en cours ....")
    risk_levels = {"Informational": 0, "Low": 0, "Medium": 0, "High": 0}
    alerts = zap.core.alerts()

    for alert in alerts:
        risk = alert.get("risk")
        if risk in risk_levels:
            risk_levels[risk] += 1

    plt.bar(risk_levels.keys(), risk_levels.values(), color=["blue", "green", "yellow", "red"])
    plt.xlabel("Niveaux de risque")
    plt.ylabel("Nombre d'alertes")
    plt.title("Nombre d'alertes par niveau de risque")
    plt.savefig("{}/{}_alertes.png".format(graphs_folder, app_url.replace("://", "_").replace("/", "_")))
    print("Graphe généré")

def main():
    zap = ZAPv2(apikey=api_key)
    
    for app_url in apps:
        print("Scannage de l'application : {}".format(app_url))
        scan_app(zap, app_url)
        generate_report(zap, app_url)
        plot_alerts_by_risk(zap, app_url)

        print("\n")
        print("******************************************************")

if __name__ == "__main__":
    main()
