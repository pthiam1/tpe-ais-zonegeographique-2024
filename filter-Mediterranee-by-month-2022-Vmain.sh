Coords="-5.9820513 36.0565049 -5.234981 34.8032836 -2.3785357 34.8393599 10.1458784 36.8342068 9.1351362 33.5673398 19.4622847 29.7913995 22.186894 32.0903357 28.8226362 30.3618207 35.3265425 31.1548458 36.7767378 37.2551127 29.6136518 37.2900829 26.6253706 40.9370356 14.0130659 46.0948246 3.8177534 43.7300946 -5.9820513 36.0565049"

echo "#############################@"
date;python3 -u main.py -sd "2022-01-01 00:00:00" -ed "2022-01-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee"
date;python3 -u main.py -sd "2022-02-01 00:00:00" -ed "2022-02-28 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee"
date;python3 -u main.py -sd "2022-03-01 00:00:00" -ed "2022-03-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee"
date;python3 -u main.py -sd "2022-04-01 00:00:00" -ed "2022-04-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee"
date;python3 -u main.py -sd "2022-05-01 00:00:00" -ed "2022-05-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee"
date;python3 -u main.py -sd "2022-06-01 00:00:00" -ed "2022-06-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee"
date;python3 -u main.py -sd "2022-07-01 00:00:00" -ed "2022-07-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee"
date;python3 -u main.py -sd "2022-08-01 00:00:00" -ed "2022-08-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee"
date;python3 -u main.py -sd "2022-09-01 00:00:00" -ed "2022-09-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee"
date;python3 -u main.py -sd "2022-10-01 00:00:00" -ed "2022-10-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee"
date;python3 -u main.py -sd "2022-11-01 00:00:00" -ed "2022-11-30 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee"
date;python3 -u main.py -sd "2022-12-01 00:00:00" -ed "2022-12-31 23:59:59" -pol $Coords -srcdir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Jour" -tardir "/mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee"
date;ls -l /mnt/PROJET-CIRMAR2/AisData/AISHUB/CSV/2022-Mediterranee/*.csv
date
echo "#############################@"

