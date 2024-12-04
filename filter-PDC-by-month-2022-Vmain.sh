Coords="0.9987522 49.8318826 1.663425 49.8602204 2.0094944 50.6852465 3.5530735 51.3247021 0.8888889 51.6837218 0.2681614 50.8832078 0.9987522 49.8318826"

echo "#############################@"
date;python3 -u main.py -sd "2022-01-01 00:00:00" -ed "2022-01-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDF"
date;python3 -u main.py -sd "2022-02-01 00:00:00" -ed "2022-02-28 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC"
date;python3 -u main.py -sd "2022-03-01 00:00:00" -ed "2022-03-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC"
date;python3 -u main.py -sd "2022-04-01 00:00:00" -ed "2022-04-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC"
date;python3 -u main.py -sd "2022-05-01 00:00:00" -ed "2022-05-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC"
date;python3 -u main.py -sd "2022-06-01 00:00:00" -ed "2022-06-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC"
date;python3 -u main.py -sd "2022-07-01 00:00:00" -ed "2022-07-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC"
date;python3 -u main.py -sd "2022-08-01 00:00:00" -ed "2022-08-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC"
date;python3 -u main.py -sd "2022-09-01 00:00:00" -ed "2022-09-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC"
date;python3 -u main.py -sd "2022-10-01 00:00:00" -ed "2022-10-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC"
date;python3 -u main.py -sd "2022-11-01 00:00:00" -ed "2022-11-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC"
date;python3 -u main.py -sd "2022-12-01 00:00:00" -ed "2022-12-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC"
date;gzip -v /mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC/*.csv
date;ls -l /mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-PDC/*.csv
date
echo "#############################@"

