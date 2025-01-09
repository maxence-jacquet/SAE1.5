def parse_ics(file_path):
    """
    Fonction pour analyser le contenu du fichier .ics et extraire les informations nécessaires
    sous forme de dictionnaire. Les champs manquants sont complétés par 'vide'.
    """
    with open(file_path, 'r') as file:
        ics_content = file.read()
    
    event_data_global = []
    event_data = {}

    # Liste des clés attendues
    required_keys = [
        "DTSTAMP", "DTSTART", "DTEND", "SUMMARY", 
        "LOCATION", "DESCRIPTION", "UID", "CREATED", 
        "LAST-MODIFIED", "SEQUENCE"
    ]
    
    # Diviser le contenu en lignes
    lines = ics_content.splitlines()
    
    # Parcourir chaque ligne et extraire les informations clés
    for line in lines:
        line = line.strip()  # Supprimer les espaces inutiles
        if line.startswith("BEGIN:VEVENT"):
            # Début d'un nouvel événement
            event_data = {}
        elif line.startswith("END:VEVENT"):
            # Fin de l'événement, compléter les clés manquantes par 'vide'
            for key in required_keys:
                if key not in event_data:
                    event_data[key] = "Vide"
            event_data_global.append(event_data)
        elif line.startswith("DTSTAMP:"):
            event_data["DTSTAMP"] = line.replace("DTSTAMP:", "").strip()
        elif line.startswith("DTSTART:"):
            event_data["DTSTART"] = line.replace("DTSTART:", "").strip()
        elif line.startswith("DTEND:"):
            event_data["DTEND"] = line.replace("DTEND:", "").strip()
        elif line.startswith("SUMMARY:"):
            summary = line.replace("SUMMARY:", "").strip()
            event_data["SUMMARY"] = summary if summary else "Vide"  # Gérer un champ vide
        elif line.startswith("LOCATION:"):
            location = line.replace("LOCATION:", "").strip()
            event_data["LOCATION"] = location if location else "Vide"
        elif line.startswith("DESCRIPTION:"):
            # Gérer les retours à la ligne dans la description
            description = line.replace("DESCRIPTION:", "").strip()
            description = ' '.join(description.split('\\n')).strip()
            event_data["DESCRIPTION"] = description if description else "Vide"
        elif line.startswith("UID:"):
            uid = line.replace("UID:", "").strip()
            event_data["UID"] = uid if uid else "Vide"
        elif line.startswith("CREATED:"):
            created = line.replace("CREATED:", "").strip()
            event_data["CREATED"] = created if created else "Vide"
        elif line.startswith("LAST-MODIFIED:"):
            last_modified = line.replace("LAST-MODIFIED:", "").strip()
            event_data["LAST-MODIFIED"] = last_modified if last_modified else "Vide"
        elif line.startswith("SEQUENCE:"):
            sequence = line.replace("SEQUENCE:", "").strip()
            event_data["SEQUENCE"] = sequence if sequence else "Vide"
    
    return event_data_global


def filter_events(events, filter_key, filter_value):
    """
    Fonction pour filtrer les événements selon une clé et une valeur spécifiques.
    """
    filtered_events = [
        event for event in events if event.get(filter_key, "vide") == filter_value
    ]
    return filtered_events

def main():
    # Chemin du fichier .ics
    ics_file_path = "ADE_RT1_Septembre2023_Decembre2023.ics"

    # Analyse du fichier
    events = parse_ics(ics_file_path)

    # Filtre sur une valeur spécifique, par exemple "SAE1.05" dans le champ SUMMARY
    filter_key = "SUMMARY"  # Clé à filtrer
    filter_value = "SAE1.05"  # Valeur à filtrer
    filtered_events = filter_events(events, filter_key, filter_value)

    # Affichage des événements filtrés
    for event in filtered_events:
        for key, value in event.items():
            print(f"{key}: {value}")
        print("\n")
if __name__ == "__main__":
    main()