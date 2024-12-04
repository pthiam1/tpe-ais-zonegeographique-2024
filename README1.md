## Presentation du projet :

AIS est un système d'identification automatique qui permet d'échanger de façon automatique des messages entre des navires et par radio VHF. Ce système permet aux navires et au système de surveillance du trafic de connaître l’identité, le statut et la position des navires dans les zones de navigation. Il joue un rôle important dans la sécurité maritime.
 
Nous disposons d'un ensemble de fichiers au format CSV comportant des données AIS des navires du monde entier. Le but est ici de mettre à disposition un programme en python qui
permet de voir quel navire arrive dans quel port, en comparant les coordonnées de géolocalisation des navires avec celles des ports.

### Travail effectué :

1 **Connexion à la base de données**

Tout d'abord, il faut créer une base de données et insérer toutes les données du fichier CSV
qui contient tous les ports du monde.

 - **Installer la librairie psycopg2**
 
**psycopg2** permet de se connecter à une base de données PostGreSQL et de l’interroger. Il s’agit d’un adaptateur de bases de données PostGreSQL qui est à la fois très utilisé, léger et efficace.
 
Sous Linux, son installation relativement simple se fait de la façon suivante :

*pip install psycopg2*

Pour l’installer sous l’environnement Mac OS X, il suffira de procéder de la façon suivante :

*pip install psycopg2*

*pip install psycopg2-binary*
 
2. **Description du programme :**

2.1 **Filtrage des colonnes d'un fichier csv :**

*Filtercsv.py* permet de filtrer les colonnes d'un fichier CSV pour garder que les colonnes nécessaires et diminuer la taille du fichier. Le résultat est stocké dans le fichier resultat.csv

![alt text](Images/filtre-colonnes.png)
![alt text](Images/res-filtre-colonnes.png)

2.1 **Boundingbox :**

Cette méthode permet de délimiter la zone géographique sous forme d'un rectangle, 
elle prend en paramètre un point(latitude / longitude) de la zone, et la distance en km, 
et elle renvoi une liste de coordonnées (latitude minimale, latitude maximale, longitude minimale, longitude maximale).

 ![alt text](Images/box.png)
 
 **Exemple de test sur cette méthode :**
 
 *FilterBox.py*
 
Nous avons tester notre programme avec les coordonnées GPS d'un port qui se situe au Japon puis appliqué la méthode boundingBox pour délimiter une zone. Nous vérifions si les coordonnées GPS des navires dans le fichier déja filtré, sont dans la zone ou pas.<br />

![alt text](Images/compare-coord.png)

S'il y a des navires dans la zone, la méthode renvoie un fichier csv *res1.csv* qui contient des informations sur ces navires.<br />
Sinon, elle renvoit un fichier CSV vide.

![alt text](Images/res-compare.png)

**Méthode folium :**

Après avoir obtenu le fichier *res1.csv* des navires qui sont dans la zone, il est possible de  l'afficher sur une carte grâce à la méthode folium, qui lit le fichier csv et renvoi un fichier html qui affiche une carte, avec des points qui correspondent aux coordonnées de géolocalisation des navires.

![alt text](Images/folium.png)
![alt text](Images/nav_japan.png)
