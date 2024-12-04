Coords="-71.1873425 -32.4196835 -73.2088268 -32.066583 -75.4280651 -39.6080768 -73.2967175 -40.0131617 -71.1873425 -32.4196835"

echo "#############################@"
date;python3 -u main.py -sd "2022-01-01 00:00:00" -ed "2022-01-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili"
date;python3 -u main.py -sd "2022-02-01 00:00:00" -ed "2022-02-28 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili"
date;python3 -u main.py -sd "2022-03-01 00:00:00" -ed "2022-03-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili"
date;python3 -u main.py -sd "2022-04-01 00:00:00" -ed "2022-04-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili"
date;python3 -u main.py -sd "2022-05-01 00:00:00" -ed "2022-05-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili"
date;python3 -u main.py -sd "2022-06-01 00:00:00" -ed "2022-06-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili"
date;python3 -u main.py -sd "2022-07-01 00:00:00" -ed "2022-07-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili"
date;python3 -u main.py -sd "2022-08-01 00:00:00" -ed "2022-08-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili"
date;python3 -u main.py -sd "2022-09-01 00:00:00" -ed "2022-09-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili"
date;python3 -u main.py -sd "2022-10-01 00:00:00" -ed "2022-10-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili"
date;python3 -u main.py -sd "2022-11-01 00:00:00" -ed "2022-11-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili"
date;python3 -u main.py -sd "2022-12-01 00:00:00" -ed "2022-12-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili"
date;gzip -v /mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili/*.csv
date;ls -l /mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Chili/*.csv
date
echo "#############################@"

