import AIS_FileFilter2 as ais_fil
import argparse
import os
from datetime import datetime
import re
import time
import tracemalloc
from AIS_Exception import AIS_Exception
import csv
import cProfile

# TODO think about the possible errors from the user and exception/errors from the program
# WARNING If you get process stopped this means that there is too much data to handle
# what file must contains

FILE_LITTERALS = ['aishub-data-', '.csv', 'result']  # Initialisation d'une liste de trois chaînes de caractères pour la recherche de fichiers
NUMBER_OF_FILE = 0                                   # Compteur de fichiers trouvés
TABLEAU_MMSI = set()                                 # Tableau pour stocker les numéros MMSI trouvés
#Main class, Search for the files and process the arguments given by the user
class AIS_filtered_data :
    # constructor
    def __init__(self) -> None:
        self.args = self.commands()
        self.check_args()

    # adds commands with argparser and return a list of args
    def commands(self):
        """ manage the arguments """
        # Initialize the argparse parser and add description, usage and epilog
        parser = argparse.ArgumentParser(description="Arguments and their features",
                                         usage='%(prog)s [-h] [-sd STARTINGDATE] [-ed ENDINGDATE] [-pol POLYGON] [-mm MMSI] [-mt MSG_TYPE] [-t TARGET]',
                                         epilog="Use -h or --help to see more about arguments")

        # Add arguments to the parser
        parser.add_argument(
            '-sd', '--startingdate', help='Enter date in the following format : YYYY-MM-DD HH:MM:SS', type=str,
            metavar='2020-01-01 00:00:00', required=True)  # Starting date argument
        parser.add_argument(
            '-ed', '--endingdate', help='Enter date in the following format : YYYY-MM-DD HH:MM:SS', type=str,
            metavar='2020-01-01 00:30:00', required=True)  # Ending date argument
        parser.add_argument(
            '-pol', '--polygon', help="Enter coordinates", nargs="+", default=None, type=float, metavar='x1 y1 x2 y2',
            required=False)  # Polygon argument with multiple float values
        parser.add_argument('-mt', '--msg_type', help='get rows by message type',
                            type=int, default=-1, metavar='1', nargs="+",
                            required=False)  # Message type argument with multiple integer values
        parser.add_argument('-mm', '--mmsi', help='get rows depending of mmsi type',
                            type=int, metavar='12345678', default=-1, nargs="+",
                            required=False)  # MMSI argument with multiple integer values
        parser.add_argument('-srcdir', '--source_directory', help='Directory where the file to read are',
                            type=str, metavar='/path/to/folder', required=True)  # Target directory argument

        # Parse the arguments
        args = parser.parse_args()

        return args

    # checks if the date given by the user are correct (ie : starting date > ending date),
    # raise an exception if so
    def check_dates(self):
        """ checks if the date given by the user are correct (ie : starting date > ending date), raise an exception if so """
        starting_date_str = str(self.args.startingdate)
        starting_date_obj = datetime.strptime(
        starting_date_str, '%Y-%m-%d %H:%M:%S')

        ending_date_str = str(self.args.endingdate)
        ending_date_obj = datetime.strptime(
        ending_date_str, '%Y-%m-%d %H:%M:%S')
        if ending_date_obj < starting_date_obj:
            raise AIS_Exception(
                "The ending date must be superior to the starting date !")

    def check_mmsi(self):
        """ Check the mmsi """
        pass

    def check_msg_type(self):
        """ Check the msg type """
        pass

    def check_polygon(self):
        """ Check the polygon """
        # the length of the polygon must be an even number
        if self.args.polygon != None and len(self.args.polygon) % 2 != 0:
            raise AIS_Exception("The number of polygon cordinates must be an even number, actual length : {}".format(
                len(self.args.polygon)))

    # check the arguments
    def check_args(self):
        """ check the arguments """
        # for future improvement
        self.check_dates()
        self.check_mmsi()
        self.check_msg_type()
        self.check_polygon()


    #Cette méthode filtre les fichiers csv correspondant aux dates données en argument
    def file_is_in_date(self, file):

        # Extraire l'heure dans le du fichier à filtrer
        file_date = file[len(file) - 12:len(file) - 4]
        jour=file_date[6:8]
        mois=file_date[4:6]
        annee=file_date[0:4]
        datefichier=datetime(int(annee),int(mois),int(jour))
        date_obj = datetime.strptime(str(datefichier), "%Y-%m-%d %H:%M:%S")
        # Vérifier si l'heure dans le du fichier à filtrer est dans la plage horaire spécifiée en argument
        startingtimestamp = datetime.strptime(self.args.startingdate,
                                              "%Y-%m-%d %H:%M:%S")
        endingtimestamp = datetime.strptime(self.args.endingdate,
                                            "%Y-%m-%d %H:%M:%S")
        #print(self.args.startingdate,datefichier,self.args.endingdate)
        #print(startingtimestamp, date_obj, endingtimestamp)
        if startingtimestamp <= date_obj <= endingtimestamp:
            return True
        print("Le fichier",file,"ne sera pas analysé car il ne correspond pas aux dates")
        return False

    def filter_files(self):
        hascsv = 0
        isaishub = 0
        global TABLEAU_MMSI
        global NUMBER_OF_FILE
        number_of_row_in_the_csv_file = 0
        est_ligne_valide = None
        tracemalloc.start()
        start = time.time()

        # Vérifie que le dossier ciblé n'est pas vide
        if len(list(os.scandir(self.args.source_directory))) == 0:
            raise AIS_Exception('Folder is empty')

        # Création du fichier de sortie
        original_filename = self.fichier_sortie()
        with open(original_filename, 'w', newline='') as csvWfile:
            header = None  # la premiere ligne du fichier csv
            writer = csv.writer(csvWfile, delimiter=';')

            # Parcours des fichiers dans le dossier ciblé
            listedesfichiers=sorted(os.listdir(self.args.source_directory))
            #print(listedesfichiers)
            for file in listedesfichiers:
                files_with_path = None
                file_data = None

                # Traitement des fichiers CSV
                if file.endswith('.csv'):
                    print(f"Processing file: {file}")
                    hascsv += 1
                    regex = re.compile(r"aishub-data-\d{1,}.csv")
                    matches = regex.match(file)

                    # Vérification que le fichier CSV est au bon format
                    if matches is not None:
                        file_that_matched = matches.group(0)
                        isaishub += 1

                        #si le fichier est concerné par l'intervalle de date
                        if self.file_is_in_date(file):
                            NUMBER_OF_FILE += 1

                            #on crée une instance de la classe AIS_Filter2 avec les arguments donnés pas l'utilisateur pour faire le filtrage
                            files_with_path = os.path.join(self.args.source_directory, file)
                            file_data = ais_fil.AIS_Filter2(filename=files_with_path, coords=self.args.polygon,
                                                            startingdate=self.args.startingdate,
                                                            endingdate=self.args.endingdate, mmsi=self.args.mmsi,
                                                            msg_type=self.args.msg_type)

                            # Ouverture du fichier en lecture
                            with open(file_data.filename, "r", newline="") as csvRfile:
                                start_reading = False #elle permet de derterminer si on a atteint la premiere ligne qui contient
                                                      # la date de début afin de commencer le traitement sur cette ligne
                                notindate = None # elle permet de determiner si on est arrivé sur une ligne qui a une date
                                                 # supérieur à endingDate, afin d'arreter le traitement surcette ligne
                                firstline=True
                                for line in csvRfile:
                                    row = line.strip().split(';')
                                    if header is None:
                                        header = row
                                        writer.writerow(header) # si c'est l'entête on l'écrit
                                    else:
                                        if firstline:
                                            firstline=False
                                            #print(firstline)
                                        elif not start_reading:
                                            # print(datetime.strptime(row[0], "%d/%m/%Y %H:%M:%S"), datetime.strptime(self.args.startingdate, "%Y-%m-%d %H:%M:%S") )
                                            if datetime.strptime(row[0], "%d/%m/%Y %H:%M:%S") == datetime.strptime(
                                                    self.args.startingdate, "%Y-%m-%d %H:%M:%S") or datetime.strptime(
                                                    row[0], "%d/%m/%Y %H:%M:%S") >= datetime.strptime(
                                                    self.args.startingdate, "%Y-%m-%d %H:%M:%S"):
                                                #print(row[0])
                                                start_reading = True
                                        else:
                                            #si l'utilisateur n'a pas donné de coordonnées, on fait le filtre avec la date, (le ou les MMSI et type de message, s'ils sont donnés)
                                            startingtimestamp = datetime.strptime(file_data.startingdate,
                                                                                  "%Y-%m-%d %H:%M:%S")
                                            endingtimestamp = datetime.strptime(file_data.endingdate,
                                                                                "%Y-%m-%d %H:%M:%S")
                                            if self.args.polygon is None:
                                                est_ligne_valide = file_data.ship_filter(header, row,startingtimestamp,endingtimestamp)
                                                if est_ligne_valide in ["in MMSI and in Message_Types", "in MMSI", "in Message_Types", "no MMSI and Message_types"]:
                                                    #print("in date")
                                                    writer.writerow(row)

                                                    number_of_row_in_the_csv_file += 1
                                                elif est_ligne_valide in ["not in MMSI and in Message_Types", "not in MMSI", "not in Message_Types"]:
                                                    pass
                                                else:
                                                    notindate = True
                                            else:
                                                # si l'utilisateur a donné de coordonnées
                                                est_ligne_valide = file_data.isInsideUserPolygonChecker(header, row, startingtimestamp, endingtimestamp)
                                                if  est_ligne_valide == "in polygone":
                                                    writer.writerow(row)

                                                    number_of_row_in_the_csv_file += 1
                                                    if self.has_message_type5():
                                                        #on garde le MMSI de la ligne si l'utilisateur à donné le type de message 5
                                                        TABLEAU_MMSI.add(row[3])
                                                    else:
                                                        pass
                                                elif est_ligne_valide == "not in polygone":
                                                    pass
                                                #gestion des messages de type 5
                                                elif est_ligne_valide == "message type 5":
                                                    #si le MMSI est dans la liste des messages des navires qui sont dans la zone, on garde la ligne
                                                    if len(TABLEAU_MMSI) != 0 and row[3] in TABLEAU_MMSI:
                                                        #print("type 5",row[1])
                                                        writer.writerow(row)

                                                        number_of_row_in_the_csv_file += 1
                                                    else:
                                                        pass
                                                else:
                                                    notindate = True
                                        if notindate:
                                            break
                    print(f"Finished processing file: {file}") #fin du traitement d'un fichier
            csvWfile.flush()
            print("All files processed.") #fin du traitement de tous les fichiers
        #s'il n'y a pas de fichier csv dans le repertoire, on lance une exception
        if hascsv == 0:
            raise AIS_Exception("No CSV file in the specified folder")
        #s'il n'y a pas de fichier qui commence par aishub, on lance une exception
        if isaishub == 0:
            raise AIS_Exception("No aishub csv in this directory")

        #on affiche apres excecution, le temps d'execution, le nombre de fichier traités, ...
        nb_file_in_targeted_directory = len(list(os.scandir(self.args.source_directory)))
        end = time.time()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10 ** 6}MB\nPeak was {peak / 10 ** 6}MB")
        tracemalloc.stop()
        print("Time elapsed : {} s".format((end - start)))
        print("Number of files in the targeted directory : {}".format(nb_file_in_targeted_directory))
        print("Number of file treated : " + str(NUMBER_OF_FILE))
        print("Number of rows in the csv file : " + str(number_of_row_in_the_csv_file))
        print(f"Treated file has a size of {os.path.getsize(original_filename) / 10 ** 6}MB")
        print(f"Written data in {original_filename}")

    # Méthode permettant de créer et de retourner le nom du fichier de sortie original_filename
    def fichier_sortie(self):
        # On convertit les dates en string et on remplace les espaces par des underscores
        startingdate = str(self.args.startingdate).replace(' ', '_')
        endingdate = str(self.args.endingdate).replace(' ', '_')

        # Si l'argument mmsi est donné, on ajoute le numéro MMSI au nom du fichier
        if self.args.mmsi != -1:
            partmmsi = "_mmsi_" + str(self.args.mmsi)
        else:
            partmmsi = ""
        # Si l'argument msg_type est donné, on ajoute le type de message au nom du fichier
        if self.args.msg_type != -1:
            partmsgtype = "_msg_type_" + str(self.args.msg_type)
        else:
            partmsgtype = ""

        # On crée le nom de fichier complet en concaténant les différentes parties avec les littéraux de fichier
        original_filename = FILE_LITTERALS[0] + \
                            startingdate + '_to_' + endingdate + partmmsi + partmsgtype + FILE_LITTERALS[1]
        # On remplace les deux points dans le nom de fichier par des tirets
        original_filename = original_filename.replace(":", "-")

        # On retourne le nom de fichier complet
        return original_filename

    #elle permet de vérifier si l'utilisateur a donné le type de message 5 sur ses arguments
    def has_message_type5(self):

        if (isinstance(self.args.msg_type, int)):
            if self.args.msg_type==-1:
                listmsg=[5]
        else:
            listmsg=self.args.msg_type
        if 5 in listmsg:
            return True
        return False

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    ais_filt = AIS_filtered_data()
    ais_filt.filter_files()
    profiler.disable()
    #profiler.print_stats()
    cProfile.run('AIS_filtered_data().filter_files()')