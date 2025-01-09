import numpy as np
import csv

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
        heure = txt_split2[0]
        IP_source = txt_split2[1]

        txt_split5 = txt_split[1].split(": ")
        IP_destination = txt_split5[0]
        txt_split6 = txt_split5[1]
        txt_split7 = txt_split6.split(", ")

        txt_flag = txt_split7[0]
        txt_seq = txt_split7[1] if len(txt_split7) > 1 else ""
        txt_ack = txt_split7[2] if len(txt_split7) > 2 else ""
        txt_win = txt_split7[3] if len(txt_split7) > 3 else ""
        txt_contenu_option = f"[{txt_split7[4]}]" if len(txt_split7) > 4 and 'options' in txt_split7[4] else ""
        txt_leght = txt_split7[-1] if txt_split7 else ""

        evenement = f"{heure};{IP_source};{IP_destination};{txt_flag};{txt_seq};{txt_ack};{txt_win};{txt_contenu_option};{txt_leght}"
        valeur.append(evenement)

lecture()

# Écriture du CSV
titre = "heure;IP_source;IP_destination;flag;seq;ack;win;option;leght"
with open(r'C:\Users\maxen\Desktop\Maxence\IUT\BUT1\S1\SAE 1.5 Traiter des données\SAE1.5 GitHub\Projet\projet_sae1.5.csv', 'w', newline='') as fichiercsv:
    writer = csv.writer(fichiercsv, delimiter=';')
    writer.writerow(titre.split(";"))
    for row in valeur:
        writer.writerow(row.split(";"))

print("Données écrites dans projet_sae1.5.csv")
