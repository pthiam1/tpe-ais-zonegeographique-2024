# tpe-ais-zonegeographique-2023

- Année : **M1 IWOCS**
- Matière: *TPE*

## Auteurs

|Nom| Prénom       |
|--|--------------|
*SOUNG* | *Mame Fatou* |
*EL OUAZI* | *Oualid*      |

## Travail demandé
Le travail demandé était de récrire le code de filtrage en utilisant la bibliothèque csv de python (donc supprimer polars),
ensuite faire le filtrage comme suit : 
- Parcourir chaque fichier du repertoire donné en argument ;
- Pour chaque fichier, on vérifie s'il est concerné par l'intervalle de date donné en argument ;
- Si oui, on l'ouvre en lecture, le parcourir ligne par ligne en faisant le filtrage selon les arguments donnés en ligne de commande 
(MMSI, type de message, coordonnées polygone);
- Et si une ligne est vérifié, on l'écrit dans le fichier de sortie et on passe à la ligne suivante.

## Approche utilisée
Pour faire ce travail, nous avons modifié principalement les fichiers **AIS_ Simplificator.py** et **AIS_FileFilter**.
Nous avons réécrit ces 2 classes dans les fichiers respectifs AIS_filtered_data.py et AIS_FileFilter2.py.
Cependant, il y a certaines méthodes que nous avons conservées qui n'utilisent pas polars comme : 
- Le constructeur de la classe **AIS_Simplificator**;
- La méthode _commands(self)_ de la classe **AIS_Simplificator** : qui permet d'ajouter les commandes avec argparser ;
- La méthode _check_args(self)_ de la classe **AIS_Simplificator** : qui permet de vérifier la validité des arguments ;
- Le constructeur et la méthode _polygon_coords_translator(self)_ de la classe **AIS_FileFilter**.

## La classe AIS_FileFilter2
Dans cette classe, nous avons redéfini les 2 méthodes _ship_filter()_ et _isInsideUserPolygonChecker()_,
qui font toujours la même chose, mais en utilisant la bibliothèque csv au lieu de polars.
### ship_filter(self,header,row) : 
Elle permet de faire le filtrage sans coordonnées géographiques.
Elle prend en argument l'en tete du fichier csv et une ligne pour vérifier si la ligne correspond aux arguments de filtrage donné par l'utilisateur ou non.
### isInsideUserPolygonChecker(self,header,row): 
Elle permet de faire le filtrage sur une zone définie à partir des coordonnées données par l'utilisateur.
Elle prend en argument l'en tete du fichier csv et une ligne pour vérifier si le navire correspondant est dans la zone et qu'il correspond aux autres arguments de recherche.

## La classe AIS_filtered_data
Elle est la classe principale.
Nous avons redéfini les méthodes suivantes : 
### file_is_in_date(self, file):
Pour vérifier si un fichier _file_ correspond aux dates données en argument.
### filter_files(self):
Avec la premiere version (**AIS_Simplificator** avec **polars**), on avait les méthodes :
- _get_files(self)_ : elle retourne une liste de fichiers csv dans le répertoire donné en argument, qui correspondent à certains critères
(l'extension des fichiers doit être '.csv', les noms des fichiers doivent correspondre à une expression régulière définie par le modèle "aishub-data-\d{1,}-\d{1,}.csv",
les fichiers doivent correspondre à la plage de dates spécifiée dans les arguments et la méthode retourne une liste de chemins d'accès complets à ces fichiers.)
- _read_files(self)_ : elle lit les fichiers renvoyés par la méthode _get_files_ bet produit un dataframe à partir des données extraites.
- _benchmark(self)_ : elle lit les fichiers à partir de la méthode _read_files_ et écrit les données lues dans un fichier de sortie.
elle affiche aussi des informations telles que la taille du fichier écrit, la quantité de données écrites dans le fichier et le nom du fichier.

Maintenant avec notre version, nous avons regroupé toutes ces 3 méthodes dans une seule (filter_files(self)).\
1. elle Vérifie que le dossier ciblé n'est pas vide ;
2. Si c'est le cas, elle parcourt chaque fichier dans le dossier ciblé ;
3. Vérifie que le fichier CSV est au bon format et s'il est concerné par l'intervalle de date ;
4. Si oui, elle crée une instance de la classe AIS_Filter2 avec les arguments donnés pas l'utilisateur et ouvre le fichier en lecture ;
5. Lit le fichier ligne par ligne en faisant appel à la méthode selon les arguments donnés pour faire le filtrage ;
6. À la fin on obtient on fichier de sortie contenant les lignes filtrées, et on affiche les détails du traitement
(le temps d'exécution, le nombre de fichier traités, ...).
Nous avons gérer aussi les messages de type 5 en même temps.

## Résultat obtenu
Apres l'implémentation des différentes méthodes décrite précédemment, nous avons obtenu un programme qui marche et qui donne le bon résultat.\
Cependant, nous avons eu un souci avec le temps d'exécution.\
En effet, nous avons d'abord testé notre programme sur un petit fichier contenant 4857 lignes et nous avons obtenu un faible temps d'execution.\
Ensuite, nous avons testé sur des fichiers de grande taille contenant plus d'un million de lignes et le temps d'execution était de 200 et quelques secondes.\

## Optimisation du programme
Pour résoudre le problème du temps d'exécution, nous avons utilisé sur l'argument _endingDate_.\
Par exemple : 
- exemple 1 : si l'utilisateur veut avoir les messages entre "22/01/2020 à 11:00:00" et "22/012020 à 11:00:30",
le traitement prend du temps, environ 100 secondes. On voit bien que le filtrage ne concerne que les premieres ligne du fichier.
Mais le programme va parcourir tout le fichier, même les lignes qui sont hors de _endingDate_.

- exemple 2 : si l'utilisateur veut avoir les messages entre "**22/01/2020 à 11:59:00**" et "**22/012020 à 12:00:30**" sachant que chaque fichier ne contient que des données sur 1h,
donc ça implique 2 fichiers différents (**aishub-data-22012020-11.csv** et **aishub-data-22012020-12.csv**).\
Le traitement du fichier de **12h** passe en moins d'une seconde, mais celui de **11h** prend beaucoup de temps.
Cela est du par le fait que le programme parcourt toutes les lignes du fichier en commençant par la premiere
et que les lignes correspondant à la date "**11:59:00**" sont à la fin du fichier. 

La premiere solution que nous avons trouvé est d'arrêter le parcourt du fichier si toute fois, on rencontre une ligne avec une date supérieure à _endingDate_.
Cette solution permet de résoudre le problème de l'exemple 1, mais elle n'est fiable que si l'utilisateur fait son filtre sur les premiere lignes (exemple 1).

Et pour résoudre le problème de l'exemple 2, nous devons trouver un moyen de commencer la lecture à la premiere ligne du fichier contenant la valeur de _startingDate_.\
Cela n'est possible qu'avec l'utilisation de pandas ou de polars.

## Quelques commandes pour tester le code
- python3 -u AIS_filtered_data.py -sd "2021-01-22 00:00:00" -ed "2021-01-22 00:59:50" -mt 1 4 -tardir "/home/msoung/M1_IWOCS/TPE/tpe-ais-zonegeographique-2023/fichier_csv"
- python3 -u AIS_filtered_data.py -sd "2020-01-22 11:00:00" -ed "2020-01-22 11:00:30" -mm 230044260 265663280 440191310 356068000 -mt 5 18 -tardir "/home/msoung/M1_IWOCS/TPE/tpe-ais-zonegeographique-2023/fichier_csv"
- python3 -u AIS_filtered_data.py -sd "2020-01-22 11:00:00" -ed "2020-01-22 11:00:30" -mt 1 4 -pol 0 0 200 0 0 -200 200 -200 100 -300 0 200 200 200 -tardir "/home/msoung/M1_IWOCS/TPE/tpe-ais-zonegeographique-2023/fichier_csv"
- python3 -u AIS_filtered_data.py -sd "2020-01-22 11:00:00" -ed "2020-01-22 11:00:30" -mt 1 5 18 -pol 0 0 200 0 0 -200 200 -200 100 -300 0 200 200 200 -tardir "/home/msoung/M1_IWOCS/TPE/tpe-ais-zonegeographique-2023/fichier_csv"

