import time
from zapv2 import ZAPv2
import os
import sys

def scan(target):
    print(f"Scan en cours de l'application web : {target}")                                         #Le scannage avec zaproxy se fait en deux étapes : Le spidering et le active scan
    zap.urlopen(target)                                                                             #Le spidering en fait c'est l'étape oû le zap explore tout les répertoires existants dans l'application web.
    time.sleep(2)                                                                                   #Le active scan est l'étape du scannage proprement dit. Le scannage de tout les répertoires énumérés par le spider
                                                                                                       
                                                                                                    #La commande qui lance le spidering est zap.spider.scan() 
    print("Spidering target...")                                                                    #La commande zap.spide.status() affiche en fait le pourcentage d'évolution du spider
    spider_id = zap.spider.scan(target)                                                             #Donc tant que le statut n'est pas venu a 100%, l'opération s'arrête pas.
    while int(zap.spider.status(spider_id)) < 100:                                                  #Le time sleep c'est pour dire au script d'attendre un peu avant de vérifier à nouveau le pourcentage de l'opération en cours
        time.sleep(2)                                                                               #Ca permet d'éviter de surcharger l'API de Zaproxy avec des requêtes assez fréqeuntes.
    print("Spider completed.")


    print("Demmarage du active scan")
    active_scan_id = zap.ascan.scan(target)
    while int(zap.ascan.status(active_scan_id)) < 100:  #ascan = active scan
        time.sleep(5)

    print("Active scan fini.") 

def generate_report(target, report_format="html"):
    output_file = f"{target.replace('://', '_').replace('/', '_')}.{report_format}"
    if report_format == "html":
        with open(output_file, "wb") as f:
            f.write(zap.core.htmlreport().encode('utf-8'))                                          #wb = write binary. IL es utilisé parce que l'encodage utf-8 converti les chaines de caractères du rapport HTML en objet bytes
                                                                                                    #La méthode write() attend un objet bytes pour écrire dans un fichier en mode binaire.
    elif report_format == "xml":                                                                    #Le with, garanti que le fichier sera correctement fermé après avoir terminé l'écriture du rapport
        with open(output_file, "wb") as f:
            f.write(zap.core.xmlreport().encode('utf-8'))
    else:
        print("Invalid report format")
        sys.exit(1)
    print(f"Report saved to {output_file}")


def read_targets_from_txt(file_path):
    with open(file_path, "r") as f:
        targets = [line.strip() for line in f.readlines()]
    return targets



if __name__ == "__main__":
    api_key = "eav40kgfuit23effcc7ao36tl2"
    zap = ZAPv2(apikey=api_key)

    urls = input("Please put the path of your text file : ")

    targets = read_targets_from_txt(urls)

    for target in targets:
        scan(target)
        generate_report(target, report_format="html")  # nous pouvons changer le format du rapport ici ("html" ou "xml")
        print("\n")
