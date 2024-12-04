Coords="161.7866636 -19.2859115 162.1821714 -23.6200321 168.4883237 -23.7809877 168.4883237 -19.4103017 161.7866636 -19.2859115"

echo "#############################@"
date;python3 -u main.py -sd "2022-01-01 00:00:00" -ed "2022-01-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie"
date;python3 -u main.py -sd "2022-02-01 00:00:00" -ed "2022-02-28 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie"
date;python3 -u main.py -sd "2022-03-01 00:00:00" -ed "2022-03-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie"
date;python3 -u main.py -sd "2022-04-01 00:00:00" -ed "2022-04-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie"
date;python3 -u main.py -sd "2022-05-01 00:00:00" -ed "2022-05-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie"
date;python3 -u main.py -sd "2022-06-01 00:00:00" -ed "2022-06-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie"
date;python3 -u main.py -sd "2022-07-01 00:00:00" -ed "2022-07-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie"
date;python3 -u main.py -sd "2022-08-01 00:00:00" -ed "2022-08-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie"
date;python3 -u main.py -sd "2022-09-01 00:00:00" -ed "2022-09-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie"
date;python3 -u main.py -sd "2022-10-01 00:00:00" -ed "2022-10-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie"
date;python3 -u main.py -sd "2022-11-01 00:00:00" -ed "2022-11-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie"
date;python3 -u main.py -sd "2022-12-01 00:00:00" -ed "2022-12-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie"
date;gzip -v /mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie/*.csv
date;ls -l /mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-NouvelleCaledonie/*.csv
date
echo "#############################@"

