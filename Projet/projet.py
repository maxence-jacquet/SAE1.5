import markdown
import webbrowser

# Lecture du fichier
with open(r"C:\Users\maxen\Desktop\Maxence\IUT\BUT1\S1\SAE 1.5 Traiter des données\SAE1.5 GitHub\Projet\DumpFile.txt", "r") as fh:
    ress = fh.read().split('\n')

valeur = []

def lecture():
    for row in ress:
        if row.startswith("\t"):
            continue
        construction_liste(row)

def construction_liste(row):
    if "IP" in row:
        txt_split = row.split(">")
        txt_split2 = txt_split[0].split("IP")
        heure = txt_split2[0].strip()
        IP_source_with_port = txt_split2[1].strip()

        # Extraire le port source
        if '.' in IP_source_with_port:
            IP_source, port_source = IP_source_with_port.rsplit(".", 1)
        else:
            IP_source, port_source = IP_source_with_port, "Vide"

        IP_destination_with_port = txt_split[1].split(":")[0].strip()
        if '.' in IP_destination_with_port:
            IP_destination, port_destination = IP_destination_with_port.rsplit(".", 1)
        else:
            IP_destination, port_destination = IP_destination_with_port, "Vide"

        txt_split6 = txt_split[1].split(": ")[1]
        txt_split7 = txt_split6.split(", ")

        # Gérer les colonnes optionnelles et longueur
        txt_contenu_option = f"[{txt_split7[4].strip()}]" if len(txt_split7) > 4 and 'options' in txt_split7[4] else "Vide"
        txt_leght = txt_split7[-1].strip() if txt_split7 else "Vide"

        evenement = f"{heure};{IP_source};{IP_destination};{port_source};{port_destination};{txt_contenu_option};{txt_leght}"
        valeur.append(evenement)

lecture()

# Générer le contenu Markdown avec une seule colonne pour le port
titre = "Heure;IP Source;IP Destination;Port Source;Port Destination;Option;Length"
headers = titre.split(";")
markdown_content = f"| {' | '.join(headers)} |\n"
markdown_content += f"| {' | '.join(['---'] * len(headers))} |\n"

for row in valeur:
    markdown_content += f"| {' | '.join(row.split(';'))} |\n"

# Sauvegarder dans un fichier Markdown
markdown_file = r'C:\Users\maxen\Desktop\Maxence\IUT\BUT1\S1\SAE 1.5 Traiter des données\SAE1.5 GitHub\Projet\resultat.md'
with open(markdown_file, "w", encoding="utf-8") as md_file:
    md_file.write(markdown_content)

# Convertir le Markdown en HTML avec une structure de tableau
html_content = markdown.markdown(markdown_content, extensions=['tables'])

# Ajouter une structure HTML de base pour le rendu
html_with_structure = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Résultat TCPDump</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        table, th, td {{
            border: 1px solid black;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f4f4f4;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""

# Sauvegarder dans un fichier HTML
html_file = r'C:\Users\maxen\Desktop\Maxence\IUT\BUT1\S1\SAE 1.5 Traiter des données\SAE1.5 GitHub\Projet\resultat.html'
with open(html_file, "w", encoding="utf-8") as file:
    file.write(html_with_structure)

# Ouvrir automatiquement dans le navigateur
webbrowser.open(html_file)

print(f"Tableau Markdown converti en HTML et ouvert dans le navigateur : {html_file}")
