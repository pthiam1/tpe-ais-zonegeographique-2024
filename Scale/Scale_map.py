import pandas as pd
from keplergl import KeplerGl

# Charger les données des bateaux depuis le fichier CSV
def load_boat_data(file_path):
    columns = [
        "Complete_Sys_Date", "Message_Type", "Repeat_Indicator", "MMSI", "Navigation_Status",
        "Rate_Of_Turn", "Speed_Over_Ground", "Position_Accuracy", "Longitude", "Latitude",
        "Course_Over_Ground", "True_Heading", "Time_Stamp", "Maneuver_Indicator", "Spare",
        "RAIM_flag", "Year", "Month", "Day", "Hour", "Minute", "Second", "Complete_Date",
        "Fix_Quality", "Type_Of_EPFD", "AIS_Version", "IMO_Number", "Call_Sign", "Vessel_Name",
        "Ship_Type", "Dimension_to_Bow", "Dimension_to_Stern", "Dimension_to_Port",
        "Dimension_to_Starboard", "Position_Fix_Type", "ETA_Month", "ETA_Day", "ETA_Hour",
        "ETA_Minute", "Complete_ETA_Date", "Draught", "Destination", "DTE", "CSUnit",
        "Display_Flag", "Dsc_Flag", "Band_Flag", "Name", "Ship_Type_Cargo", "Message_22_flag",
        "Assigned", "SyncState", "SlotTimeout", "SubMessage", "keep", "slotIncrement",
        "numberOfSlots", "JourSys", "MoisSys", "AnneeSys", "HeureSys", "MinSys", "SecSys"
    ]
    
    try:
        data = pd.read_csv(file_path, delimiter=';', names=columns)
        data['Longitude'] = pd.to_numeric(data['Longitude'].astype(str).str.replace(',', '.', regex=False), errors='coerce')
        data['Latitude'] = pd.to_numeric(data['Latitude'].astype(str).str.replace(',', '.', regex=False), errors='coerce')
        return data.dropna(subset=['Longitude', 'Latitude'])
    except Exception as e:
        print(f"Erreur lors du chargement des bateaux : {e}")
        return pd.DataFrame()


# Charger les données des ports depuis le fichier CSV
def load_ports_data(file_path):
    try:
        ports_data = pd.read_csv(file_path, delimiter=';', on_bad_lines="skip", engine='python')
        ports_data['LongitudeDecimal'] = pd.to_numeric(ports_data['LongitudeDecimal'].astype(str).str.replace(',', '.', regex=False), errors='coerce')
        ports_data['LatitudeDecimal'] = pd.to_numeric(ports_data['LatitudeDecimal'].astype(str).str.replace(',', '.', regex=False), errors='coerce')
        required_columns = ['LatitudeDecimal', 'LongitudeDecimal', 'PortName']
        if not all(col in ports_data.columns for col in required_columns):
            raise ValueError(f"Colonnes manquantes : {required_columns}")
        return ports_data.dropna(subset=['LatitudeDecimal', 'LongitudeDecimal'])
    except Exception as e:
        print(f"Erreur lors du chargement des ports : {e}")
        return pd.DataFrame()


# Charger les données des quais depuis le fichier CSV
def load_berths_data(file_path):
    try:
        berths_data = pd.read_csv(file_path, delimiter=';', on_bad_lines="skip", engine='python')
        berths_data['Dec_Longitude'] = pd.to_numeric(berths_data['Dec_Longitude'].astype(str).str.replace(',', '.', regex=False), errors='coerce')
        berths_data['Dec_Latitude'] = pd.to_numeric(berths_data['Dec_Latitude'].astype(str).str.replace(',', '.', regex=False), errors='coerce')
        required_columns = ['Dec_Latitude', 'Dec_Longitude', 'Berth_Name']
        return berths_data.dropna(subset=required_columns)
    except Exception as e:
        print(f"Erreur lors du chargement des quais : {e}")
        return pd.DataFrame()


# Convertir les données en GeoJSON pour Kepler
def to_geojson(data, lat_col, lon_col, props):
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [row[lon_col], row[lat_col]]},
                "properties": {key: row[key] for key in props if key in row}
            }
            for _, row in data.iterrows()
        ]
    }


# Créer une carte avec kepler.gl
def create_kepler_map(boat_data, ports_data, berths_data, output_path):
    map_ = KeplerGl()

    # Ajouter les données des bateaux
    if not boat_data.empty:
        boat_geojson = to_geojson(boat_data, "Latitude", "Longitude", ["MMSI", "Ship_Type", "Vessel_Name"])
        map_.add_data(data=boat_geojson, name="Boats")
    else:
        print("Données des bateaux vides. Pas de données ajoutées à la carte.")

    # Ajouter les données des ports
    if not ports_data.empty:
        ports_geojson = to_geojson(ports_data, "LatitudeDecimal", "LongitudeDecimal", ["PortName"])
        map_.add_data(data=ports_geojson, name="Ports")
    else:
        print("Données des ports vides. Pas de données ajoutées à la carte.")

    # Ajouter les données des quais
    if not berths_data.empty:
        berths_geojson = to_geojson(berths_data, "Dec_Latitude", "Dec_Longitude", ["Berth_Name"])
        map_.add_data(data=berths_geojson, name="Berths")
    else:
        print("Données des quais vides. Pas de données ajoutées à la carte.")

    # Sauvegarder la carte
    map_.save_to_html(file_name=output_path)
    print(f"Carte exportée vers {output_path}")


# Chemins des fichiers
boat_file_path = 'Scale/UpdatedAISData.csv'
port_file_path = 'Scale/BD-PORTS-QUAIS-TERMINAUX/Ports.csv'
berth_file_path = 'Scale/BD-PORTS-QUAIS-TERMINAUX/Berths.csv'
output_map_path = 'boats_ports_and_berths_map.html'

# Charger les données
boat_data = load_boat_data(boat_file_path)
ports_data = load_ports_data(port_file_path)
berths_data = load_berths_data(berth_file_path)

# Créer et sauvegarder la carte
create_kepler_map(boat_data, ports_data, berths_data, output_map_path)
