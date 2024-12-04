# filtrage des colonnes d'un fichier CSV
import csv
import sys
import glob
import time

data = []
files= []
# On commence par parcourir la liste des fichiers CSV situés dans le répertoire courant
# et on l'enregistre dans la liste "files"
for file in glob.glob("aishub-data*.csv"):
    files.append(file)
csv.field_size_limit(10000000)
files.sort()

# On reprend la liste des fichiers et on va les traiter
for filename in files:
    # On traite les fichiers un à un
    print("Début du traitement de "+filename+"...")
    start_time = time.time()
    data.clear()
    with open(filename,newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        for row in csvreader:
            data.append([
                row[0],
                row[1],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
                row[9],
                row[10],
                row[11],
                row[25],
                row[26],
                row[28],
                row[29],
                row[40]
                ])
        next(csvreader, None)

        file_name = "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-LaReunion-Filtered/"+filename.split(".")[0]+"-filtered.csv"
        
        with open(file_name, "w", newline="") as file:
            for d in data:
                csv.writer(file).writerow(d)
            print("... Fichier filtré !")

        print(file_name+" has been created in {:5.4f} seconds".format(time.time() - start_time))