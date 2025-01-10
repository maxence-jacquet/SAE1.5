import matplotlib.pyplot as plt

# Lecture du fichier
try:
    with open(r"C:\Users\maxen\Desktop\Maxence\IUT\BUT1\S1\SAE 1.5 Traiter des données\SAE1.5 GitHub\Projet\DumpFile.txt", "r", encoding='utf-8') as fh:
        ress = fh.read().split('\n')

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
            IP_source_with_port = txt_split2[1].strip()
            IP_destination_with_port = txt_split[1].split(":")[0].strip()

            # Extraire le port source et destination
            IP_source, port_source = IP_source_with_port.rsplit(".", 1) if '.' in IP_source_with_port else (IP_source_with_port, "Vide")
            IP_destination, port_destination = IP_destination_with_port.rsplit(".", 1) if '.' in IP_destination_with_port else (IP_destination_with_port, "Vide")

            ip_sources.append(IP_source)
            ip_destinations.append(IP_destination)

    lecture()

    # Fonction pour traiter les données et générer les diagrammes
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
            ip_others['Autre'] = autre_count

        ip_top.extend(ip_others.items())
        labels = [f"{type_ip} - {label}" for label, count in ip_top]
        sizes = [count for label, count in ip_top]

        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title(f'Repartition des {type_ip} avec seuil de {seuil}%')
        plt.axis('equal')  # Assurer que le diagramme est circulaire

        # Enregistrement du diagramme en PNG
        plt.savefig(f"{type_ip}_Diagramme.png")
        plt.close()  # Fermeture de la figure pour éviter l'affichage automatique

    # Diagramme pour les IP Sources
    generer_diagrammes(ip_sources, 'IP Source', 5)

    # Diagramme pour les IP Destinations
    generer_diagrammes(ip_destinations, 'IP Destination', 5)

except FileNotFoundError:
    print("Le fichier DumpFile.txt n'existe pas.")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")
