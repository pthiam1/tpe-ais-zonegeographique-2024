from datetime import datetime
from shapely.geometry import Point, Polygon
from ast import literal_eval
import polars as pl
import sys
"""
    Classe permettant de manipuler les fichiers
"""
class AIS_Filter:
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

    def read_file(self):
        """ Create a dataframe """
        # polars will read the csv with all the columns considered as utf8 when the parameters infer_schema_length = 0, the useful columns will have an appropriate dtypes
        df = pl.read_csv(file=self.filename, sep=";", has_header=True,infer_schema_length=0)
        df=df.lazy().with_columns([
            # to not change the type/value of complete sys date in the end we need to create another column that we will use for computations
            pl.col("Complete_Sys_Date").str.strptime(pl.Datetime, fmt="%d/%m/%Y %H:%M:%S").alias('Complete_Sys_Date_Alt'),
            pl.col('MMSI').cast(pl.Int64, strict=True),
            pl.col('Message_Type').cast(pl.Int64, strict=True),]).collect()
        return df
    # create a column with a datetime format from different column that store date info
    
    """
        Fonction de conversion des dates de début et de fin
    """
    def timeChecker(self):
        """ Convert to datetime format the starting and ending date """
        startingtimestamp = datetime.strptime(
            self.startingdate, '%Y-%m-%d %H:%M:%S')
        endingtimestamp = datetime.strptime(self.endingdate, '%Y-%m-%d %H:%M:%S')

        return startingtimestamp, endingtimestamp

    # convert polygon coords given by the user into appropriate type
    """
        Fonction de conversion des coordonnées du polygone fournit en entrée
        en un type approprié (retourne une liste)
    """
    def polygon_coords_translator(self):
        """ Translate the coordonates given by the user into the format desire by the shapely package """
        raw_data = self.coords        
        tuppleList = []
        # put each pair of value in a list
        for i in range(0, len(raw_data), 2):
            tuppleList.append((raw_data[i], raw_data[i + 1]))
        
        return tuppleList 
        
        
    # add a column that inform if a ship is inside the polygon (final filter if coords are give)
    """
        Si les coordonnées du navire sont dans le polygone, 
        on ajoute une colonne pour le signaler
    """
    def isInsideUserPolygonChecker(self) -> pl.DataFrame:
        """ Create a column that tells if the ship is inside the polygon given by the user """
        df = self.ship_filter()
        # if the df is empty no need to do complex computations (ie no ships found on that period)
        if df.is_empty():
            # all dataframe need to have a isInside column even if it's empty
            #df['isInside'] = []
            #df = df.lazy().with_columns(pl.col('isInside').cast(pl.Boolean)).collect()
            return df
        polygon = Polygon(self.polygon_coords_translator())

        #optimized version of the commented lines
        df=df.lazy().with_columns([
            pl.col('Longitude').apply(lambda s: float(str(s).replace(',', '.'))).alias('PersonnalLongitude'),
            pl.col('Latitude').apply(lambda s: float(str(s).replace(',', '.'))).alias('PersonnalLatitude'),
        ]).collect()
    
        # Consider None values as 0.0 coordinates (bad way)
        """ df = df.lazy().with_column(pl.when(pl.col('Longitude') == None).then(
            '0.0').otherwise(pl.col("Longitude")).alias("Longitude")).collect()
        df = df.lazy().with_column(pl.when(pl.col('Latitude') == None).then(
            '0.0').otherwise(pl.col("Latitude")).alias("Latitude")).collect()  """
        df = df.lazy().with_columns([
            pl.format("({},{})", "PersonnalLongitude", "PersonnalLatitude").alias("Position"),
        ]).collect()
        # filter on the none values
        df=df.lazy().filter(pl.col('Position')!="(None,None)").collect()
        # evaluate each string as a tupple then create a point object that allows us to see if it's inside the user polygon or not
        df=df.lazy().with_column(pl.col('Position').apply(lambda s:polygon.contains(Point(literal_eval(str(s))))).alias('isInside')).collect()
        # check if a point is inside the polygon
        #df=df.lazy().with_column(pl.col('Position').apply().alias('isInside')).collect()
        if 'Position' in df.columns:
            df = df.drop(['Position'])
        df= df.lazy().filter(pl.col('isInside')==True).collect()
        if 'isInside' in df.columns:
            df=df.drop(['isInside'])
        if 'PersonnalLongitude' in df.columns:
            df=df.drop(['PersonnalLongitude'])
        if 'PersonnalLatitude' in df.columns:
            df=df.drop(['PersonnalLatitude'])
        return df
    
    def filter_expr_msg_type(self)->pl.Expr:
        """ Return a pl.Expr that it is used for filtering """
        return (pl.col('Message_Type').is_in(self.msg_type))

    def filter_expr_mmsi(self)->pl.Expr:
        """ Return a pl.Expr that it is used for filtering """
        return (pl.col('MMSI').is_in(self.mmsi))

    def filter_expr_date(self)->pl.Expr:
        """ Return a pl.Expr that it is used for filtering """
        startingTimeStamp, endingTimeStamp = self.timeChecker()
        # filter on the date
        return (pl.col('Complete_Sys_Date_Alt').is_between(startingTimeStamp, endingTimeStamp))
            
    def ship_filter(self) -> pl.DataFrame:
        """ Function that Filter on date and arguments given by the user """
        df = self.read_file()
        lf = df.lazy()
        expr=pl.Expr()
        # mmsi given
        if self.mmsi!=-1:
            # msg type given
            if self.msg_type!=-1:
                expr=(self.filter_expr_mmsi() & self.filter_expr_msg_type() & self.filter_expr_date())
                
            # msg type not given
            else:
                expr=(self.filter_expr_mmsi() & self.filter_expr_date())
        # mmsi not given
        else:
            # msg_type given
            if self.msg_type!=-1:
                expr=(self.filter_expr_msg_type() & self.filter_expr_date())
        # both not given
        if self.msg_type==-1 and self.mmsi==-1:
            expr=(self.filter_expr_date())
        
         # filter on date, mmsi,
        df=lf.filter(expr).collect()
        if 'Complete_Sys_Date_Alt' in df.columns:
            df=df.drop(['Complete_Sys_Date_Alt'])
        return df
        
        #return lf.filter((pl.col('MMSI') == mmsi) & (pl.col('datetime') >= startingTimeStamp) & (pl.col('datetime') <= endingTimeStamp) & (pl.col('Latitude') != '') & (pl.col('Longitude') != '') & (pl.col('Message_Type') == msg_type)).collect()


