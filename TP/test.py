import matplotlib.pyplot as plt
from collections import Counter

def parse_ics(file_path, attribute):
    """
    Fonction pour analyser le contenu du fichier .ics et extraire les informations nécessaires
    pour un attribut donné sous forme de dictionnaire.
    """
    with open(file_path, 'r') as file:
        ics_content = file.read()

    event_data_global = []
    event_data = {}
    lines = ics_content.splitlines()
    
    for line in lines:
        line = line.strip()
        if line.startswith("BEGIN:VEVENT"):
            event_data = {}
        elif line.startswith("END:VEVENT"):
            event_data_global.append(event_data)
        elif line.startswith(f"{attribute}:"):
            value = line.replace(f"{attribute}:", "").strip()
            event_data[attribute] = value if value else "vide"

    return event_data_global

def plot_event_distribution(events, attribute, output_file):
    """
    Fonction pour créer un diagramme à barres montrant la répartition des événements
    pour un attribut donné.
    """
    # Extraire les valeurs de l'attribut des événements
    values = [event.get(attribute, "vide") for event in events]
    
    # Compter les occurrences de chaque valeur
    value_counts = Counter(values)
    
    # Données pour le diagramme
    labels = list(value_counts.keys())
    counts = list(value_counts.values())
    
    # Créer le diagramme
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color='skyblue')
    plt.xlabel(attribute, fontsize=12)
    plt.ylabel("Nombre d'événements", fontsize=12)
    plt.title(f"Répartition des événements par {attribute}", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    
    # Sauvegarder le diagramme
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Diagramme sauvegardé dans {output_file}")

def main():
    # Chemin du fichier .ics
    ics_file_path = "ADE_RT1_Septembre2023_Decembre2023.ics"
    output_image = "event_distribution.png"
    
    # Demander à l'utilisateur de choisir l'attribut
    attribute = input("Entrez l'attribut à analyser (par exemple, LOCATION, SUMMARY, DTSTART) : ").strip().upper()
    
    # Analyse du fichier
    events = parse_ics(ics_file_path, attribute)

    # Vérifier si des événements ont été trouvés pour l'attribut donné
    if not any(attribute in event for event in events):
        print(f"Aucun événement trouvé pour l'attribut {attribute}.")
        return

    # Créer et enregistrer le diagramme
    plot_event_distribution(events, attribute, output_image)

if __name__ == "__main__":
    main()
