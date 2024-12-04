from datetime import datetime
from shapely.geometry import Point, Polygon
from ast import literal_eval
import sys
import csv
from typing import List, Tuple
"""
    Classe permettant de manipuler les fichiers
"""
class AIS_Filter2:
    """class that manipulate individual file"""

    FILE_LITTERALS = ['aishub-data-', '.csv', 'result']

    """
        Constructeur de la classe avec le nom du fichier, les coordonnées
        les dates de début et de fin, le numéro MMSI et le type de message
    """
    def __init__(self, filename, coords, startingdate, endingdate, mmsi,
        msg_type) -> None:
        self.filename = filename
        self.coords = coords
        self.startingdate = startingdate
        self.endingdate = endingdate
        self.mmsi = mmsi
        self.msg_type = msg_type
        pass

    # convert polygon coords given by the user into appropriate type
    """
        Fonction de conversion des coordonnées du polygone fournit en entrée en un type approprié (retourne une liste)
    """

    def polygon_coords_translator(self):
        """Translate the coordinates given by the user into the format desired by the shapely package"""
        raw_data = self.coords

        tuppleList = [(raw_data[i], raw_data[i + 1]) for i in range(0, len(raw_data), 2)]

        return tuppleList

    #elle permet de filtrer les données selon la date, MMSI et Type de message
    def ship_filter(self,header,row,startingtimestamp,endingtimestamp):
        """Function that filters on date and arguments given by the user"""
        # get the index of each column

        date_idx = header.index('Complete_Sys_Date')
        date_obj = datetime.strptime(row[date_idx], "%d/%m/%Y %H:%M:%S")
        if startingtimestamp <= date_obj < endingtimestamp:
            mmsi_idx = header.index('MMSI')
            message_type_idx = header.index('Message_Type')

            #print(startingtimestamp, date_obj, endingtimestamp)
            # filter on MMSI
            if self.mmsi != -1 and self.msg_type != -1:
                #print("MMSI and MT")
                if int(row[mmsi_idx]) in self.mmsi and int(row[message_type_idx]) in self.msg_type:
                    return "in MMSI and in Message_Types"
                return "not in MMSI and in Message_Types"
            elif self.mmsi != -1 and self.msg_type == -1:
                #print("MMSI " + str(self.mmsi))
                if int(row[mmsi_idx]) in self.mmsi:
                    return "in MMSI"
                return "not in MMSI"
            elif self.mmsi == -1 and self.msg_type != -1:
                if int(row[message_type_idx]) in self.msg_type:
                    #print(self.msg_type, row[message_type_idx])
                    return "in Message_Types"
                return "not in Message_Types"
            else:
                #print("no MMSI no MT")
                return "no MMSI and Message_types"
        else:
            return "not in Date"

    # elle permet de filtrer les donné selon la date, MMSI et Type de message, et puis vérifie si le navire est dans la zone donnée
    def isInsideUserPolygonChecker(self, header, row,startingtimestamp,endingtimestamp):
        """ Create a column that tells if the ship is inside the polygon given by the user """
        data = self.ship_filter(header, row, startingtimestamp, endingtimestamp)
        #print(data)
        if data !="not in Date":
            longitude = None
            latitude = None
            polygon = Polygon(self.polygon_coords_translator())
            position = None
            longitude_index = header.index('Longitude')
            latitude_index = header.index('Latitude')
            #print(row)
            if data in ["not in MMSI and in Message_Types", "not in MMSI", "not in Message_Types"]:
                return "not in polygone"
            #print("okey")
            if row[longitude_index] and row[latitude_index]:
                #print("okey")
                longitude = float(row[longitude_index].replace(',', '.'))
                latitude = float(str(row[latitude_index]).replace(',', '.'))
            else:
                #print("not okey")
                longitude = 0.0
                latitude = 0.0
            position = (longitude, latitude)
            #print(polygon,Point(position))
            if longitude != 0.0 and latitude != 0.0:
                if polygon.contains(Point(position)):
                    #print("contains")
                    return "in polygone"
                else:
                    #print("not in polygone")
                    return "not in polygone"
            else:
                return "message type 5"
        return "not in Date"
