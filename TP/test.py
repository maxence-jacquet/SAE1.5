import markdown
import webbrowser
import matplotlib.pyplot as plt
import os

# Fichier d'entrée
input_file = r"C:\Users\maxen\Desktop\Maxence\IUT\BUT1\S1\SAE 1.5 Traiter des données\SAE1.5 GitHub\Projet\DumpFile.txt"

# Lecture du fichier et traitement
try:
    with open(input_file, "r", encoding="utf-8") as fh:
        ress = fh.read().split("\n")

    valeur = []
    ip_sources = []
    ip_destinations = []

    def lecture():
        for row in ress:
            if not row.startswith("\t"):
                construction_liste(row)

    def construction_liste(row):
        if "IP" in row:
            txt_split = row.split(">")
            txt_split2 = txt_split[0].split("IP")
            heure = txt_split2[0].strip()
            IP_source_with_port = txt_split2[1].strip()

            # Extraire le port source
            IP_source, port_source = IP_source_with_port.rsplit(".", 1) if "." in IP_source_with_port else (IP_source_with_port, "Vide")

            IP_destination_with_port = txt_split[1].split(":")[0].strip()
            IP_destination, port_destination = IP_destination_with_port.rsplit(".", 1) if "." in IP_destination_with_port else (IP_destination_with_port, "Vide")

            txt_split6 = txt_split[1].split(": ")[1]
            txt_split7 = txt_split6.split(", ")

            # Gérer les colonnes optionnelles et longueur
            txt_contenu_option = f"[{txt_split7[4].strip()}]" if len(txt_split7) > 4 and "options" in txt_split7[4] else "Vide"
            txt_leght = txt_split7[-1].strip() if txt_split7 else "Vide"

            evenement = f"{heure};{IP_source};{IP_destination};{port_source};{port_destination};{txt_contenu_option};{txt_leght}"
            valeur.append(evenement)

            # Ajouter aux listes pour les diagrammes
            ip_sources.append(IP_source)
            ip_destinations.append(IP_destination)

    lecture()

    # Générer le contenu Markdown
    titre = "Heure;IP Source;IP Destination;Port Source;Port Destination;Option;Length"
    headers = titre.split(";")
    markdown_content = f"| {' | '.join(headers)} |\n"
    markdown_content += f"| {' | '.join(['---'] * len(headers))} |\n"

    for row in valeur:
        markdown_content += f"| {' | '.join(row.split(';'))} |\n"

    # Sauvegarde du tableau Markdown et conversion en HTML
    markdown_file = os.path.join(os.path.dirname(input_file), "resultat.md")
    html_file = os.path.join(os.path.dirname(input_file), "resultat.html")
    diagramme_html_file = os.path.join(os.path.dirname(input_file), "diagrammes.html")
    
    with open(markdown_file, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

    html_content = markdown.markdown(markdown_content, extensions=["tables"])
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
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(html_with_structure)

    webbrowser.open(html_file)

    # Générer des diagrammes circulaires
    def generer_diagrammes(ip_list, type_ip, seuil):
        ip_count = {}
        for ip in ip_list:
            ip_count[ip] = ip_count.get(ip, 0) + 1

        sorted_ips = sorted(ip_count.items(), key=lambda x: x[1], reverse=True)
        total_count = sum(ip_count.values())
        autre_count = 0
        ip_top = []
        ip_others = {}

        for ip, count in sorted_ips:
            if (count / total_count) * 100 < seuil:
                autre_count += count
            else:
                ip_top.append((ip, count))

        if autre_count > 0:
            ip_others["Autre"] = autre_count

        ip_top.extend(ip_others.items())
        labels = [f"{label}" for label, count in ip_top]
        sizes = [count for label, count in ip_top]

        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
        plt.title(f"Répartition des {type_ip}")
        plt.axis("equal")

        diagramme_file = os.path.join(os.path.dirname(input_file), f"{type_ip}_Diagramme.png")
        plt.savefig(diagramme_file)
        plt.close()

        return diagramme_file

    # Générer les fichiers PNG pour les diagrammes
    diagramme_ip_source = generer_diagrammes(ip_sources, "IP Source", 5)
    diagramme_ip_destination = generer_diagrammes(ip_destinations, "IP Destination", 5)

    # Générer une page HTML pour afficher les diagrammes
    diagramme_html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Diagrammes TCPDump</title>
    </head>
    <body>
        <h1>Diagrammes des IP</h1>
        <h2>IP Source</h2>
        <img src="{os.path.basename(diagramme_ip_source)}" alt="Diagramme des IP Sources">
        <h2>IP Destination</h2>
        <img src="{os.path.basename(diagramme_ip_destination)}" alt="Diagramme des IP Destinations">
    </body>
    </html>
    """

    with open(diagramme_html_file, "w", encoding="utf-8") as file:
        file.write(diagramme_html_content)

    # Ouvrir la page HTML contenant les diagrammes
    webbrowser.open(diagramme_html_file)

    print(f"Tableau Markdown converti en HTML et ouvert dans le navigateur : {html_file}")
    print(f"Diagrammes enregistrés et affichés dans : {diagramme_html_file}")

except FileNotFoundError:
    print("Le fichier DumpFile.txt n'existe pas.")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")
