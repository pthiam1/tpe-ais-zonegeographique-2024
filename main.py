import argparse
import gzip

import AIS_Exception
import time
from datetime import datetime
import csv
import sys
import glob
from shapely.geometry import Point, Polygon
import os

FILE_LITTERALS = ['aishub-data-', '.csv', 'result']  # Initialisation d'une liste de trois chaînes de caractères pour la recherche de fichiers
NUMBER_OF_FILE = 0                                   # Compteur de fichiers trouvés
TABLEAU_MMSI = set()                                 # Tableau pour stocker les numéros MMSI trouvés
TABLEAU_MMSI_5 = set()                               # Tableau pour stocker les numéros MMSI trouvés

# adds commands with argparser and return a list of args
"""
On défini les différents arguments que l'on souhaite passer en ligne de commande avec la librairie ArgParser
"""
def commands():
    """ manage the arguments """
    # Initialize the argparse parser and add description, usage and epilog
    parser = argparse.ArgumentParser(description="Arguments and their features",
                                     usage='%(prog)s [-h] [-sd STARTINGDATE] [-ed ENDINGDATE] [-pol POLYGON] [-mm MMSI] [-nt LISTNUM] [-mt MSG_TYPE] [-srcdir SOURCE] [-tardir TARGET]',
                                     epilog="Use -h or --help to see more about arguments")

    # Add arguments to the parser
    # Date de démarrage du filtrage
    parser.add_argument(
        '-sd', '--startingdate', help='Enter date in the following format : YYYY-MM-DD HH:MM:SS', type=str,
        metavar='2020-01-01 00:00:00', required=True)  # Starting date argument
    # Date de fin du filtrage
    parser.add_argument(
        '-ed', '--endingdate', help='Enter date in the following format : YYYY-MM-DD HH:MM:SS', type=str,
        metavar='2020-01-01 00:30:00', required=True)  # Ending date argument
    # Zone géographique définie pour le filtrage
    parser.add_argument(
        '-pol', '--polygon', help="Enter coordinates", nargs="+", default=None, type=float, metavar='x1 y1 x2 y2',
        required=False)  # Polygon argument with multiple float values
    # Type de message à retenir
    parser.add_argument('-mt', '--msg_type', help='get rows by message type',
                        type=int, default=-1, metavar='1', nargs="+",
                        required=False)  # Message type argument with multiple integer values
    # Identifiant MMSI des navires à filtrer
    parser.add_argument('-mm', '--mmsi', help='get rows depending of mmsi type',
                        type=int, metavar='t1 t2 t3...', default=-1, nargs="+",
                        required=False)  # MMSI argument with multiple integer values
    # Type des navires à retenir
    parser.add_argument('-nt', '--navire_type', help='entrer different navire type',
                        type=int, metavar='t1 t2 t3...', default=-1, nargs="+",
                        required=False)  # MMSI argument with multiple integer values
    # Répertoire source des données à traiter
    parser.add_argument('-srcdir', '--source_directory', help='Directory where the file to read are',
                        type=str, metavar='/path/to/folder', required=True)  # Source directory argument
    # Répertoire de destination des données traitées
    parser.add_argument('-tardir', '--target_directory', help='Directory where the file to read are',
                        type=str, metavar='/path/to/folder', required=True)  # Target directory argument

    # Parse the arguments
    args = parser.parse_args()
    # Tableau des identifiants MMSI à retenir
    TABLEAU_MMSI=args.mmsi
    return args
"""
Affichage des arguments saisies
"""
def affiche_args(args):
    print ("###########################################################################################")
    print ("Les arguments saisis sont les suivants :")
    print ("- Date de début des données à prendre en considération :              ", args.startingdate)
    print ("- Date de fin des données à prendre en considération :                ", args.endingdate)
    print ("- Coordonnées de la zone géographique considérée:                     ", args.polygon)
    print ("- Type de messages AIS à retenir :                                    ", args.msg_type)
    print ("- Numéro MMSI des navires à considérer :                              ", args.mmsi)
    print ("- Type des navires à considérer :                                     ", args.navire_type)
    print ("- Répertoire source où se trouvent les fichiers CSV à analyser :      ", args.source_directory)
    print ("- Répertoire de destination où enregistrer les fichiers CSV produits :", args.target_directory)
    print ("###########################################################################################")

# checks if the date given by the user are correct (ie : starting date > ending date),
# raise an exception if so
"""
Vérification des dates saisies
"""
def check_dates(args):
    """ checks if the date given by the user are correct (ie : starting date > ending date), raise an exception if so """
    starting_date_str = str(args.startingdate)
    starting_date_obj = datetime.strptime(starting_date_str, '%Y-%m-%d %H:%M:%S')

    ending_date_str = str(args.endingdate)
    ending_date_obj = datetime.strptime(ending_date_str, '%Y-%m-%d %H:%M:%S')
    if ending_date_obj < starting_date_obj:
        raise AIS_Exception("The ending date must be superior to the starting date !")

"""
Vérification des coordonnées du polygone
"""
def check_polygon(args):
    """ Check the polygon """
    # the length of the polygon must be an even number
    if args.polygon != None and len(args.polygon) % 2 != 0:
        raise AIS_Exception("The number of polygon cordinates must be an even number, actual length : {}".format(len(args.polygon)))

"""
Cette méthode filtre les fichiers csv correspondant aux dates données en argument
"""
def file_is_in_date(args, filename):
    # Extraire l'heure dans le du fichier à filtrer
    # Pour un fichier CSV
    #file_date = filename[len(filename) - 12:len(filename) - 4]
    # Pour un fichier CSV gzippé
    file_date = filename[len(filename) - 15:len(filename) - 7]
    jour=file_date[6:8]
    mois=file_date[4:6]
    annee=file_date[0:4]
    datefichier=datetime(int(annee),int(mois),int(jour))
    date_obj = datetime.strptime(str(datefichier), "%Y-%m-%d %H:%M:%S")
    # Vérifier si l'heure dans le du fichier à filtrer est dans la plage horaire spécifiée en argument
    startingtimestamp = datetime.strptime(args.startingdate, "%Y-%m-%d %H:%M:%S")
    endingtimestamp = datetime.strptime(args.endingdate, "%Y-%m-%d %H:%M:%S")
    #print(args.startingdate,datefichier,args.endingdate)
    #print(startingtimestamp, date_obj, endingtimestamp)
    if startingtimestamp <= date_obj <= endingtimestamp:
        return True
    #print("Le fichier",file,"ne sera pas analysé car il ne correspond pas aux dates")
    return False

"""
Méthode permettant de créer et de retourner le nom du fichier de sortie original_filename
"""
def fichier_sortie(args):
    # On convertit les dates en string et on remplace les espaces par des underscores
    startingdate = str(args.startingdate).replace(' ', '_')
    endingdate = str(args.endingdate).replace(' ', '_')

    # On crée le nom de fichier complet en concaténant les différentes parties avec les littéraux de fichier
    original_filename = args.target_directory+"/"+FILE_LITTERALS[0] + startingdate + '_to_' + endingdate + FILE_LITTERALS[1]
    # On remplace les deux points dans le nom de fichier par des tirets
    original_filename = original_filename.replace(":", "-")

    # On retourne le nom de fichier complet
    return original_filename

"""
Crée une liste de fichiers à traiter
"""
def listefichiers(args):
    data = []
    files = []
    # On commence par parcourir la liste des fichiers CSV situés dans le répertoire courant
    # et on l'enregistre dans la liste "files"
    # Ajout de gz pour prendre en compte les fichiers gzippés 13/02/2024
    for file in glob.glob(args.source_directory+"/aishub-data-????????.csv.gz"):
        if file_is_in_date(args, file):
            files.append(file)
    csv.field_size_limit(1000000000)
    # Trie de la liste des fichiers dans l'ordre alphabétique
    files.sort()
    return files

"""
Traduit les coordonnées données par l'utilisateur dans le format souhaité par la librairie shapely.
"""
def polygon_coords_translator(args):
    """Translate the coordinates given by the user into the format desired by the shapely package"""
    raw_data = args.polygon
    tuppleList = [(raw_data[i], raw_data[i + 1]) for i in range(0, len(raw_data), 2)]
    return tuppleList


"""
Vérifie si la ligne comporte des coordonnées géographiques
"""
def is_row_with_coords(row):
    if row[8] and row[9]:
        return True
    return False

"""
Est-ce que le message est de type 5
"""
def is_msg_type_5(row):
    if row[1]=="5":
        return True
    return False

"""
Méthode vérifiant que la ligne est bien dans la zone géographique considérée
"""
def isInsideUserPolygonChecker(args, row):
    try:
        polygon = Polygon(polygon_coords_translator(args))
        longitude = float(row[8].replace(',', '.'))
        latitude  = float(row[9].replace(',', '.'))
        position = (longitude, latitude)
        if polygon.contains(Point(position)):
            return True
        else:
            return False
    except:
        return True
"""
On vérifie s'il y a des types de navires défini (>0) et si c'est le cas si la ligne concerne un de ces types de navires.
"""
def isNavireTypeCorrect(args, row):
    if args.navire_type>0:
        navire_type = int(row[29])
        if navire_type in args.navire_type:
            return True
        else:
            return False
    else:
        return True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = []
    # On commence par récupérer la liste des arguments passés en ligne de commande
    arguments=commands()
    # On affiche la liste des arguments
    affiche_args(arguments)
    # On vérifie qu'il s'agit bien d'un polygone'
    check_polygon(arguments)
    # On vérifie le format des dates données en argument
    check_dates(arguments)
    # On affiche le nom du fichier de sortie
    #print("Nom du fichier à créer :",fichier_sortie(arguments))
    #print("Liste des fichiers à traiter :",listefichiers(arguments))
    # On recupère la liste des fichiers présents dans le dossier source
    files = listefichiers(arguments)
    # On initialise une variable permettant de compter le nombre de fichiers traité
    nombre_fichiers=0
    start_time_global = time.time()
    # nom du fichier en sortie
    file_output = fichier_sortie(arguments)
    # Si le fichier existe déjà on le supprime
    if os.path.exists(file_output):
        os.remove(file_output)
    TABLEAU_MMSI = arguments.mmsi

    # On parcours la liste des fichiers à traiter
    for filename in files:
        nombre_fichiers+=1
        # On traite les fichiers un à un
        print("Début du traitement de " + filename + "...")
        start_time = time.time()
        data.clear()
        # Début du traitement du fichier
        with gzip.open(filename, mode="rt") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            ligne=0
            for row in csvreader:
                ligne += 1
                # S'il s'agit du premier fichier traité et que c'est la premiere ligne du fichier, on l'ajoute en sortie
                if nombre_fichiers==1 and ligne==1:
                    data.append([row[0], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                 row[11], row[25], row[26], row[28], row[29], row[40]])
                    #print(data)
                elif ligne != 1:
                    # Si c'est une ligne avec coordonnées
                    if is_row_with_coords(row):
                        # si la ligne est dans la zone géographique considérée et que le type de navire correspond ou n'est pas précisé
                        if isInsideUserPolygonChecker(arguments, row) and isNavireTypeCorrect(arguments, row):
                            # Si le tableau des MMSI est vide ou que le MMSI est dans le tableau
                            #print(len(TABLEAU_MMSI), TABLEAU_MMSI)
                            if len(TABLEAU_MMSI)==0 or int(row[3]) in TABLEAU_MMSI:
                                data.append(
                                    [row[0], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                     row[11], row[25], row[26], row[28], row[29], row[40]])
                                # On l'ajoute pour les messages de type 5
                                TABLEAU_MMSI_5.add(row[3])
                        else:
                            # S'il est en dehors de la zone
                            if row[3] in TABLEAU_MMSI_5:
                                TABLEAU_MMSI_5.discard(row[3])
                    # Si c'est un message de type 5
                    elif is_msg_type_5(row):
                        if row[3] in TABLEAU_MMSI_5:
                            data.append(
                                [row[0], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                 row[11], row[25], row[26], row[28], row[29], row[40]])
                            #TABLEAU_MMSI_5.add(row[3])
            next(csvreader, None)

            with open(file_output, "a", newline="") as file:
                for d in data:
                    csv.writer(file).writerow(d)
        print("Fichier traité en {:5.4f} secondes".format(time.time() - start_time))
    print(file_output + " a été créé en {:5.4f} secondes".format(time.time() - start_time_global))
