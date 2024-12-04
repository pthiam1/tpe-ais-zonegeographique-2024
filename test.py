import csv
def filter_by_polygone(file,polygon):
    """ use the coordinates to filter the ships that are inside the polygone"""
    chosing_mmsi = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        i = 0
        for row in reader:

            if i == 0 :
                # pour passer la premiere ligne ou il y a les noms des colonnes à la place des valeurs
                i += 1
                continue
            else :
                print(row[3])
                if row[8] != '' and row[9] != '':
                    x = float(row[8].replace(",", "."))
                    y = float(row[9].replace(",", "."))
                    if point_in_polygon(x, y, polygon):
                        chosing_mmsi.append(row[3])

                # x = float(row[8])
                # y = float([row[9]])
               # print(float(x))


            # if x != str and y != str:
            #     print(x, y)
            #     if point_in_polygon(x, y, polygon):
            #         chosing_mmsi.append(row[3])
            #     else:
            #         pass
            #
            #
            # else :
            #     pass

    return(chosing_mmsi)


def point_in_polygon(x, y, polygon):
    """
    Determines if a point with given coordinates (x, y) is inside a polygon made by 5 coordinates.

    Args:
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.
        polygon (list of tuples): The polygon made by 5 coordinates. Each coordinate is a tuple of (x, y) values.

    Returns:
        bool: True if the point is inside the polygon, False otherwise.
    """

    # Initialize the crossing count
    crossing_count = 0

    # Loop through each edge of the polygon
    for i in range(len(polygon)):
        # Get the start and end points of the edge
        start_point = polygon[i]
        end_point = polygon[(i + 1) % len(polygon)] # Wrap around to the beginning of the polygon for the last edge

        # Check if the edge crosses the ray
        if ((start_point[1] > y) != (end_point[1] > y)) and \
            (x < (end_point[0] - start_point[0]) * (y - start_point[1]) / (end_point[1] - start_point[1]) + start_point[0]):
            crossing_count += 1

    # If the crossing count is odd, the point is inside the polygon
    return crossing_count % 2 == 1


if __name__ == "__main__" :

    # Define the polygon as a list of 5 (x, y) coordinate tuples
    polygon = [(140, -40), (140, -31), (125, -31), (150, -40), (145, -35)]
    print(filter_by_polygone('fichier_csv/aishub-data-22012021-00.csv',polygon))
    # Test the function with a point that is inside the polygon
    x = 2
    y = 1
    print(point_in_polygon(x, y, polygon))  # True

    # Test the function with a point that is outside the polygon
    x = 0
    y = 0
    print(point_in_polygon(x, y, polygon))  # False