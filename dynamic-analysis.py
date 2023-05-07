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

def scan_app(zap, app_url):                                                                        #Le scannage avec zaproxy se fait en deux étapes : Le spidering et le active scan
    zap.urlopen(app_url)                                                                           #Le spidering en fait c'est l'étape oû le zap explore tout les répertoires existants dans l'application web.
    time.sleep(2)                                                                                  #Le active scan est l'étape du scannage proprement dit. Le scannage de tout les répertoires énumérés par le spider
                                                                                                   #La commande qui lance le spidering est zap.spider.scan() 
    spider_id = zap.spider.scan(url=app_url, apikey=api_key) 
    print(spider_id)                                      #La commande zap.spider.status() affiche en fait le pourcentage d'évolution du spider
    while int(zap.spider.status(spider_id)) < 100:                                                          #Donc tant que le statut n'est pas venu a 100%, l'opération s'arrête pas.
                                                                                                   #Le time sleep c'est pour dire au script d'attendre un peu avant de vérifier à nouveau le pourcentage de l'opération en cours
        time.sleep(5)                                                                              #Ca permet d'éviter de surcharger l'API de Zaproxy avec des requêtes assez fréqeuntes.
    print("Spider completed.")

    asscan_id = zap.ascan.scan(url=app_url, apikey=api_key)
    while int(zap.ascan.status(asscan_id)) < 100:
        time.sleep(5)
    print("Asscan completed")

def generate_report(zap, app_url):
    report_file = "{}/{}_report.html".format(reports_folder, app_url.replace("://", "_").replace("/", "_"))
    with open(report_file, "wb") as f:
        f.write(zap.core.htmlreport(api_key))

def plot_alerts_by_risk(zap):
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
    plt.savefig("{}/alertes_par_niveau_de_risque.png".format(graphs_folder))
    plt.show()

def main():
    zap = ZAPv2(proxies={"http": "http://localhost:{}".format(zap_port), "https": "http://localhost:{}".format(zap_port)})
    
    for app_url in apps:
        print("Scannage de l'application : {}".format(app_url))
        scan_app(zap, app_url)
        generate_report(zap, app_url)
        plot_alerts_by_risk(zap)

if __name__ == "__main__":
    main()
