# filtrage des colonnes d'un fichier CSV
import csv
import sys
import glob
import time

import Connexion
import poly


liste = poly.boundingBox(latitudeInDegrees=-22.25, longitudeInDegrees=166.335, halfSideInKm=2000)

lat_min = liste[0]
long_min = liste[1]
lat_max = liste[2]
long_max = liste[3]

data = []
files = []
for file in glob.glob("fichier_csv/*.csv"):
    files.append(file)
csv.field_size_limit(10000000)
for filename in files:
    # Debut du decompte du temps
    start_time = time.time()

    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        #next(csvreader, None)
        row=next(csvreader, None)
        data.append(row)
        """data.append([
                    row[0],
                    row[3],
                    row[8],
                    row[9],
                ])"""
        for row in csvreader:
            #long_nav = float(row[2])
            #lat_nav = float(row[3])
            long_nav = row[8].replace(",", ".")
            lat_nav = row[9].replace(",", ".")

            if row[0] != '..' and row[1] != '..' and long_nav != '':
                long_nav = float(long_nav)
                lat_nav = float (lat_nav)
                if (long_min <= long_nav <= long_max) and (lat_min <= lat_nav <= lat_max):
                    data.append(row)
        
                    """data.append([
                        row[0],
                        row[1],
                        long_nav,
                        lat_nav
                    ])"""

        file_name = filename.split(".")[0]+"_zone.csv"
        with open(file_name.split("/")[1], "w", newline="") as file:
            for d in data:
                csv.writer(file, delimiter=';').writerow(d)
        print(file_name.split("/")[1]+" has been filtered by geographic area in {:5.4f} seconds".format(time.time() - start_time))
