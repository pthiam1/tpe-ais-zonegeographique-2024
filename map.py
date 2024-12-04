from math import radians

import folium
import glob

monde = folium.Map(location=[0, 0], zoom_start=2)

files = []
for file in glob.glob("*.csv"):
    files.append(file)

# On reprend la liste des fichiers et on va les traiter
for filename in files:
    fichier = open(filename,"r")

    ligne = fichier.readline()
    ligne = fichier.readline()
    try:
        while ligne != "":
            liste = ligne.split(";")
            if (liste[8]!=""):
                lon = float(liste[8].replace(",", "."))
                lat = float(liste[9].replace(",", "."))
                point = folium.Marker([lat, lon]).add_to(monde)
            ligne = fichier.readline()
    except:
        print("Exception")
    fichier.close()

monde.save("resultat.html")
