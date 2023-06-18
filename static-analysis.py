#import ansi2html
import json
import os
import subprocess
import plotly.graph_objs as go
import plotly.io as pio
import tkinter as tk
from tkinter import filedialog

#from ansi2html import Ansi2HTMLConverter

def choisir_dossier():
    root = tk.Tk()
    root.withdraw()
    dossier = filedialog.askdirectory(title="Choisissez le dossier contenant les projets à analyser par Semgrep")
    return dossier

def choisir_dossier_rules():
    root = tk.Tk()
    root.withdraw()
    dossier = filedialog.askdirectory(title="Choisissez le dossier contenant vos règles Semgrep")
    return dossier

def creer_semgrepignore(repertoire):
    semgrepignore_path = os.path.join(repertoire, '.semgrepignore')
    if not os.path.exists(semgrepignore_path):
        with open(semgrepignore_path, 'w') as f:
            f.write("# Fichier .semgrepignore\n")



def analyser_dossier_semgrep(repertoire, dossier_regles):
    semgrep_cmd = f"/home/h4ck3r/.local/bin/semgrep --config={dossier_regles} --severity 'ERROR' --max-target-bytes '100 MB' --json {repertoire}"
    try:
        print(f"Exécution de Semgrep sur le répertoire : {repertoire}...")
        semgrep_output = subprocess.check_output(semgrep_cmd, shell=True)
        return json.loads(semgrep_output)
    except subprocess.CalledProcessError as e:
        return f"Erreur lors de l'exécution de Semgrep pour {repertoire} : e.output"

def generate_html_header(output_file):
    with open(output_file, "a") as file:
        file.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport d'analyse Semgrep</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.css">
    <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.js"></script>
</head>
<body>
""")

def generate_html_footer(output_file):
    with open(output_file, "a") as file:
        file.write("""
<script>
$(document).ready( function () {
    $('.semgrep-results').DataTable();
} );
</script>
</body>
</html>
""")

def generate_semgrep_results_html(project_name, results, output_file):
    with open(output_file, "a") as file:
        file.write(f"<h2>{project_name}</h2>")
        file.write("""
<table class="semgrep-results" style="width:100%; background-color: #bbff00">
    <thead>
        <tr>
            <th style="width:10%">Chemin</th>
            <th style="width:35%">Message</th>
            <th style="width:10%">Ligne</th>
            <th style="width:10%">Colonne</th>
        </tr>
    </thead>
    <tbody>
""")
        for result in results:
            message = result['extra']['message'].lower()
            if 'injection' in message or 'xss' in message or 'command':
                file.write(f"""
        <tr>
            <td>{result['path']}</td>
            
            <td>{result['extra']['message']}</td>
            <td>{result['start']['line']}</td>
            <td>{result['start']['col']}</td>
        </tr>
""")
        file.write("""
    </tbody>
</table>
""")


# def generate_semgrep_results_html(project_name, results, output_file):
#     with open(output_file, "a") as file:
#         file.write(f"<h2>{project_name}</h2>")
#         file.write("""
# <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
# <div class="table-responsive">
#     <table class="table table-bordered">
#         <thead class="thead-light">
#             <tr>
#                 <th>Chemin</th>
#                 <th>ID de la règle</th>
#                 <th>Message</th>
#                 <th>Ligne</th>
#                 <th>Colonne</th>
#             </tr>
#         </thead>
#         <tbody>
# """)
#         for result in results:
#             file.write(f"""
#             <tr>
#                 <td>{result['path']}</td>
#                 <td>{result['check_id']}</td>
#                 <td>{result['extra']['message']}</td>
#                 <td>{result['start']['line']}</td>
#                 <td>{result['start']['col']}</td>
#             </tr>
# """)
#         file.write("""
#         </tbody>
#     </table>
# </div>
# """)

vuln_types = ["command", "static code injection", "sql injection", "xss", "code injection", "ldap injection", "xpath injection"]

def count_vuln_types(results):
    counts = dict.fromkeys(vuln_types, 0)
    for result in results:
        message = result['extra']['message'].lower()
        for vuln_type in vuln_types:
            if vuln_type in message:
                counts[vuln_type] += 1
    return counts


def generate_metrics_graph(errors_by_project, output_file):
    trace = go.Bar(
        x=list(errors_by_project.keys()),
        y=list(errors_by_project.values()),
        name="Nombre d'erreurs"
    )
    layout = go.Layout(
        title="Nombre d'erreurs par projet",
        xaxis=dict(title="Nom du projet"),
        yaxis=dict(title="Nombre d'erreurs")
    )
    fig = go.Figure(data=[trace], layout=layout)
    plot_div = pio.to_html(fig, full_html=False)
    with open(output_file, "a") as file:
        file.write(plot_div)

def generate_vuln_graph(vuln_by_project, output_file):
    traces = []
    for vuln_type in vuln_types:
        traces.append(
            go.Bar(
                x=[project for project in vuln_by_project.keys()],
                y=[errors[vuln_type] for errors in vuln_by_project.values()],
                name=vuln_type
            )
        )
    layout = go.Layout(
        title="Nombre d'erreurs par projet",
        xaxis=dict(title="Nom du projet"),
        yaxis=dict(title="Nombre d'erreurs")
    )
    fig = go.Figure(data=traces, layout=layout)
    plot_div = pio.to_html(fig, full_html=False)
    with open(output_file, "a") as file:
        file.write(plot_div)

def main():
    print("Veuillez sélectionner le répertoire contenant les projets à analyser par Semgrep:")
    repertoire_projet = choisir_dossier()

    if not os.path.exists(repertoire_projet):
        print(f"Le répertoire spécifié '{repertoire_projet}' n'existe pas.")
        return

    dossiers = [os.path.join(repertoire_projet, dossier) for dossier in os.listdir(repertoire_projet) if os.path.isdir(os.path.join(repertoire_projet, dossier))]
    total_dossiers = len(dossiers)
    dossiers_analyses = 0


    print("Veuillez sélectionner le répertoire contenant vos règles Semgrep :")
    dossier_regles = choisir_dossier_rules()

    # Définir un répertoire de sortie pour les fichiers HTML
    print("Veuillez sélectionner le répertoire qui doit contenir les résultats des analyses")
    output_directory = choisir_dossier()

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_file = os.path.join(output_directory, "rapport_semgrep.html")
    generate_html_header(output_file)

    errors_by_project = {}
    vuln_by_project = {}

    for dossier_path in dossiers:
        creer_semgrepignore(dossier_path)
        semgrep_output = analyser_dossier_semgrep(dossier_path, dossier_regles)

        if not semgrep_output:
            print(f"Aucun résultat trouvé pour {dossier_path}")
            continue

        print(f"Résultat de l'analyse Semgrep pour {dossier_path}:")
        project_name = os.path.basename(dossier_path)
        generate_semgrep_results_html(project_name, semgrep_output['results'], output_file)

        errors_by_project[project_name] = len(semgrep_output['results'])

        # Utiliser la nouvelle fonction pour compter le nombre de vulnérabilités de chaque type
        vuln_by_project[project_name] = count_vuln_types(semgrep_output['results'])

        dossiers_analyses += 1
        pourcentage = (dossiers_analyses / total_dossiers) * 100
        print(f"Progression de l'analyse : {dossiers_analyses}/{total_dossiers} ({pourcentage:.2f}%)")

    generate_metrics_graph(errors_by_project, output_file)
    generate_vuln_graph(vuln_by_project, output_file)
    generate_html_footer(output_file)

if __name__ == "__main__":
    main()
