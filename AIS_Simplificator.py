import polars as pl # Expliquer à quoi sert chaque librairie
import AIS_FileFilter as ais_fil # Séparer les librairies interne des externes
import argparse
import os
from datetime import datetime
from datetime import timedelta
import re
import time
import tracemalloc
from AIS_Exception import AIS_Exception

# TODO think about the possible errors from the user and exception/errors from the program
# WARNING If you get process stopped this means that there is too much data to handle
# what file must contains
FILE_LITTERALS = ['aishub-data-', '.csv', 'result']

# class for filtering data in file
class AIS_Simplificator:
    """ Main class, Search for the files and process the arguments given by the user """

    # constructor
    def __init__(self) -> None:
        self.args = self.commands()
        self.check_args()

    # checks if the date given by the user are correct (ie : starting date > ending date), 
    # raise an exception if so
    def check_dates(self):
        """ checks if the date given by the user are correct (ie : starting date > ending date), 
        raise an exception if so """
        starting_date_str = str(self.args.startingdate)
        starting_date_obj = datetime.strptime(
            starting_date_str, '%Y-%m-%d %H:%M:%S')

        ending_date_str = str(self.args.endingdate)
        ending_date_obj = datetime.strptime(
            ending_date_str, '%Y-%m-%d %H:%M:%S')
        if ending_date_obj < starting_date_obj:
            raise AIS_Exception(
                "The ending date must be superior to the starting date !")
        # if only the time argument are given , the ending date must be inferior of one hour
        if self.args.mmsi == -1 and self.args.msg_type == -1 and self.args.polygon == None:
            if ending_date_obj - starting_date_obj > timedelta(hours=1):
                raise AIS_Exception(
                    "The ending date must be inferior of one hour !")

    # adds commands with argparser and return a list of args
    def commands(self):
        """ manage the arguments """
        parser = argparse.ArgumentParser(description="Arguments and their features",
                                         usage='%(prog)s [-h] [-sd STARTINGDATE] [-ed ENDINGDATE] [-pol POLYGON] [-mm MMSI] [-mt MSG_TYPE] [-t TARGET]',
                                         epilog="Use -h or --help to see more about arguments")
        parser.add_argument(
            '-sd', '--startingdate', help='Enter date in the following format : YYYY-MM-DD HH:MM:SS', type=str,
            metavar='2020-01-01 00:00:00', required=True)
        parser.add_argument(
            '-ed', '--endingdate', help='Enter date in the following format : YYYY-MM-DD HH:MM:SS', type=str,
            metavar='2020-01-01 00:30:00', required=True)
        parser.add_argument(
            '-pol', '--polygon', help="Enter coordinates", nargs="+", default=None, type=float, metavar='x1 y1 x2 y2',
            required=False)
        parser.add_argument('-mt', '--msg_type', help='get rows by message type',
                            type=int, default=-1, metavar='1', nargs="+", required=False)
        parser.add_argument('-mm', '--mmsi', help='get rows depending of mmsi type',
                            type=int, metavar='12345678', default=-1, nargs="+", required=False)
        parser.add_argument('-srcdir', '--source_directory', help='Directory where the file to read are',
                            type=str, metavar='/path/to/folder', required=True)
        args = parser.parse_args()

        return args

    def filter_files_by_dates(self, files):
        """ from the dates argument get the corresponding files """
        starting_date_str = str(self.args.startingdate)
        starting_date_obj = datetime.strptime(
            starting_date_str, '%Y-%m-%d %H:%M:%S')

        ending_date_str = str(self.args.endingdate)
        ending_date_obj = datetime.strptime(
            ending_date_str, '%Y-%m-%d %H:%M:%S')

        # associate every file with their dates
        file_dates = {}
        for file in files:
            file_date = file[len(file) - 15:len(file) - 4]
            datetime_file_obj = datetime.strptime(file_date, '%d%m%Y-%H')
            file_dates.update({datetime_file_obj: file})
        filtered_files = []
        for key, value in file_dates.items():
            # date comparaison
            if key >= starting_date_obj and key < ending_date_obj:
                filtered_files.append(value)
        return filtered_files

    # NO FILTER ON THE DATE ,TAKE ALL CSV THAT MATCH THE REGEX (filtering done filter_files_by_dates)

    def get_files(self):
        """ return the files following their extension, a regex and date comparaison """
        directory_content = []
        if len(os.listdir(self.args.source_directory)) == 0:
            raise AIS_Exception('Folder is empty')
        # get all csv file in the targeted directory
        for file in os.listdir(self.args.source_directory):
            if file.endswith('.csv'):
                directory_content.append(file)
        files = []
        if len(directory_content) == 0:
            raise AIS_Exception("No CSV file in the specified folder")
        regex = r"aishub-data-\d{1,}-\d{1,}.csv"
        for file in directory_content:
            matches = re.match(regex, file)
            # try on all csv file return None if no matches
            if matches is not None:
                file_that_matched = matches.group(0)
                files.append(file_that_matched)
        # no csv that store the targeted data in the directory
        if len(files) == 0:
            raise AIS_Exception("No aishub csv in this directory")
        filtered_files = self.filter_files_by_dates(files)
        files_with_path = []
        for file in filtered_files:
            files_with_path.append(os.path.join(
                self.args.source_directory, file))
        return files_with_path
    # read files and sort them

    def read_files(self) -> pl.DataFrame:
        """ Read files and produce a dataframe from the data extracted with the Utils class """
        files = self.get_files()
        files.sort()
        df_list = []
        for file in files:
            file_data = ais_fil.AIS_Filter(filename=file, coords=self.args.polygon, startingdate=self.args.startingdate,
                                           endingdate=self.args.endingdate, mmsi=self.args.mmsi,
                                           msg_type=self.args.msg_type)
            # no polygon coords given only filter on the ships
            if self.args.polygon == None:
                df = file_data.ship_filter()
            else:
                df = file_data.isInsideUserPolygonChecker()
            #print("MMSI ",df1['MMSI'])

            original_df = pl.read_csv('fichier_csv/aishub-data-22012021-00.csv',sep=';')
            #display("origi",original_df)
            filtered_df = original_df.filter(pl.col('Message_Type') == 5)


            for v in filtered_df['MMSI'] :
                if v in df['MMSI'] :
                    cast_dtype = pl.Float64
                    new_columns = []
                    # loop through all columns and cast their data types
                    for col in df.columns:
                        print(col)
                        if col != "Complete_Sys_Date" and col != "Complete_Date":
                            if df[col].dtype == pl.Utf8:
                                new_col = df[col].str.replace(',', '.').cast(cast_dtype)
                            else:
                                new_col = df[col].cast(cast_dtype)
                            new_columns.append(new_col)
                    else :
                        pass
                    df = df.with_columns(new_columns)
                    #####################################################"
                    new_columns_1 = []
                    for col in filtered_df.columns:
                        print(col)
                        if col != "Complete_Sys_Date" and col != "Complete_Date":
                            if filtered_df[col].dtype == pl.Utf8:
                                new_col = filtered_df[col].str.replace(',', '.').cast(cast_dtype)
                            else:
                                new_col = filtered_df[col].cast(cast_dtype)
                            new_columns_1.append(new_col)
                    else :
                        pass
                    df = df.with_columns(new_columns)
                    filtered_df = filtered_df.with_columns(new_columns_1)
            #display("this df : ",df)
            #display("this df_filtered : ", filtered_df)
            df = pl.concat([df, filtered_df])
            df_list.append(df)
        #print(df_list)
        # modify the dtypes beforehand
        final_df = pl.concat(df_list)
        return final_df

    def benchmark(self):
        """ benchmark the program """
        tracemalloc.start()
        start = time.time()
        df = self.read_files()
        startingdate = str(self.args.startingdate).replace(' ', '_')
        endingdate = str(self.args.endingdate).replace(' ', '_')
        if self.args.mmsi != -1:
            partmmsi = "_mmsi_" + str(self.args.mmsi)
        else:
            partmmsi = ""
        if self.args.msg_type != -1:
            partmsgtype = "_msg_type_" + str(self.args.msg_type)
        else:
            partmsgtype = ""
        # print("mmsi:",partmmsi)
        # print("msg_type:",partmsgtype )
        original_filename = FILE_LITTERALS[0] + \
                            startingdate + '_to_' + endingdate + partmmsi + partmsgtype + FILE_LITTERALS[1]
        original_filename = original_filename.replace(":", "-")
        print("Le nom du fichier est : ", original_filename)
        ##original_filename = 'aishub-data-2021-01-01_00:00:00_to_2021-01-01_23:59:59_mmsi_-1_msg_type_-1.cs'
        df.write_csv(file=original_filename, sep=";")
        nb_file_in_targeted_directory = len(os.listdir(self.args.source_directory))
        end = time.time()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10 ** 6}MB\nPeak was {peak / 10 ** 6}MB")
        tracemalloc.stop()
        print("Time elapsed : {} s".format((end - start)))
        print("Number of files in the targeted directory : {}".format(nb_file_in_targeted_directory))
        print("Number of file treated : {}".format(len(self.get_files())))
        print("Number of rows in the dataframe : {}".format(len(df)))
        print(f"Treated file has a size of {os.path.getsize(original_filename) / 10 ** 6}MB")
        print(f"Written data in {original_filename}")

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

        # print ("Le polygone est : ")
        # print(self.args.polygon)

    # check the arguments
    def check_args(self):
        """ check the arguments """
        # for future improvement 
        self.check_dates()
        self.check_mmsi()
        self.check_msg_type()
        self.check_polygon()

    def to_csv(self):
        """ Produce a csv file from the dataframe produce by then read_files function """
        df = self.read_files()
        startingdate = str(self.args.startingdate).replace(' ', '_')
        endingdate = str(self.args.endingdate).replace(' ', '_')
        original_filename = FILE_LITTERALS[0] + \
                            startingdate + '_to_' + endingdate + "_mmsi_" + \
                            str(self.args.mmsi) + "_msg_type_" + \
                            str(self.args.msg_type) + FILE_LITTERALS[1]
        df.write_csv(file=original_filename, sep=";")
        print(f"Written data in {original_filename}")


if __name__ == "__main__":
    ais_simp = AIS_Simplificator()
    ais_simp.benchmark()
