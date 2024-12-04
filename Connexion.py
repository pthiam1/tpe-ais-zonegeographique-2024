import psycopg2

"""
Méthode de connexion à la base de données PostGreSQL
"""
def conn():
    cur = psycopg2.connect(
        host="localhost",     # Nom du serveur où se trouve la base de données
        database="filtered",  # Nom de la base de données
        user="postgress",     # Nom de l'utilisateur
        password="23091996"   # Mot de passe de l'utilisateur
    )
    return cur

