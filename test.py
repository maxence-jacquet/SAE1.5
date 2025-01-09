import matplotlib.pyplot as plt
from collections import Counter

def parse_ics(file_path):
    """
    Fonction pour analyser le contenu du fichier .ics et extraire les informations nécessaires
    sous forme de dictionnaire.
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
        elif line.startswith("LOCATION:"):
            location = line.replace("LOCATION:", "").strip()
            event_data["LOCATION"] = location if location else "vide"

    return event_data_global

def plot_event_distribution(events, output_file):
    """
    Fonction pour créer un diagramme à barres montrant la répartition des événements par salle.
    """
    # Extraire les salles des événements
    locations = [event.get("LOCATION", "vide") for event in events]
    
    # Compter les occurrences de chaque salle
    location_counts = Counter(locations)
    
    # Données pour le diagramme
    labels = list(location_counts.keys())
    counts = list(location_counts.values())
    
    # Créer le diagramme
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color='skyblue')
    plt.xlabel("Salles", fontsize=12)
    plt.ylabel("Nombre d'événements", fontsize=12)
    plt.title("Répartition des événements par salle", fontsize=14)
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

    # Analyse du fichier
    events = parse_ics(ics_file_path)

    # Créer et enregistrer le diagramme
    plot_event_distribution(events, output_image)

if __name__ == "__main__":
    main()
