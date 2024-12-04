import Connexion

"""
Méthode pour l'alimentation des ports au sein de la base de données PostGreSQL
"""
def alim():
    # Connexion à la base de données 
    curseur = Connexion.conn().cursor()
    if curseur:
        print("Connexion etablie")

    # Alimentation de la table ports qui contient tout les ports du monde
    print("Début de l'importation des ports ...")

    # Ouverture de fichier  Ports.csv en mode lecture
    with open("Ports.csv", 'r') as fp:
        next(fp)
        # La méthode readlines () lit jusqu'à la fin de fichier, et retourne une liste contenant les lignes
        lignes = fp.readlines()

    # Pour chaque ligne lu dans le fichier, on la découpe et on insère les champs dans la base de données
    for ligne in lignes:
        infos = ligne.split(";", 10)
        # insertion des données dans la table Ports

        curseur.execute("INSERT INTO Ports(ID, GlobalPortID, WorldPortNumber, MasterPOID, PortName, "
                        "AlternativeName, Status, Country, Latitude, Longitude) "
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (infos[0], infos[1], infos[2], infos[3], infos[4],
                         infos[5], infos[6], infos[7], infos[8].replace(",", "."), infos[9].replace(",", ".")))
    # La méthode commit () : enregistre toutes les modifications apportées depuis le dernier commit dans la base de données.
    Connexion.conn().commit()
    print("... importation terminée !")

    curseur.close()
