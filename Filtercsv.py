# filtrage des colonnes d'un fichier CSV
import csv
import sys
import glob

import Connexion

data = []
files= []
# On commence par parcourir la liste des fichiers CSV situés dans le répertoire "fichier_csv"
# et on l'enregistre dans la liste "data"
for file in glob.glob("fichier_csv/*.csv"):
    files.append(file)
csv.field_size_limit(10000000)
#filename = 'fichier_csv/aishub-data-22012021-00.csv'
# On reprend la liste des fichiers et on va les traiter
for filename in files:
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
            long_nav = row[8].replace(",", ".")
            lat_nav = row[9].replace(",", ".")

            if row[0] != '..' and row[1] != '..' and long_nav != '':
                data.append(row)
        
                """data.append([
                    row[0],
                    row[3],
                    long_nav,
                    lat_nav
                ])"""

        file_name = filename.split(".")[0]+"filtered.csv"
        print(file_name+" has been created")
        with open(file_name, "w", newline="") as file:
            for d in data:
                csv.writer(file, delimiter=';').writerow(d)
            print("... Fichier filtré !")
