Coords="30.39211353370265 -81.72027733345023 70.21684492673884 -22.361146236353058 69.61323350083238 20.002133556321784 14.482870902270847 -16.384583270734616 -0.6533436136415237 9.1036971024515 4.4197935085662285 -7.6915313548828035 4.35184899770937 9.071907316272892 -48.57293987098463 23.798824339784808 -55.576763947818776 -65.32226634439012 -7.533993313219487 -36.84570482400287"

echo "#############################@"
date;python3 AIS_Simplificator.py -sd "2021-01-01 00:00:00" -ed "2021-01-31 23:59:59" -pol $Coords -tardir "/mnt/PROJET-CIRMAR/AisData/AISHUB/CSV/2021-dgz"
date;python3 AIS_Simplificator.py -sd "2021-02-01 00:00:00" -ed "2021-02-28 23:59:59" -pol $Coords -tardir "/mnt/PROJET-CIRMAR/AisData/AISHUB/CSV/2021-dgz"
date;python3 AIS_Simplificator.py -sd "2021-03-01 00:00:00" -ed "2021-03-31 23:59:59" -pol $Coords -tardir "/mnt/PROJET-CIRMAR/AisData/AISHUB/CSV/2021-dgz"
date;python3 AIS_Simplificator.py -sd "2021-04-01 00:00:00" -ed "2021-04-30 23:59:59" -pol $Coords -tardir "/mnt/PROJET-CIRMAR/AisData/AISHUB/CSV/2021-dgz"
date;python3 AIS_Simplificator.py -sd "2021-05-01 00:00:00" -ed "2021-05-31 23:59:59" -pol $Coords -tardir "/mnt/PROJET-CIRMAR/AisData/AISHUB/CSV/2021-dgz"
date;python3 AIS_Simplificator.py -sd "2021-06-01 00:00:00" -ed "2021-06-30 23:59:59" -pol $Coords -tardir "/mnt/PROJET-CIRMAR/AisData/AISHUB/CSV/2021-dgz"
date;python3 AIS_Simplificator.py -sd "2021-07-01 00:00:00" -ed "2021-07-31 23:59:59" -pol $Coords -tardir "/mnt/PROJET-CIRMAR/AisData/AISHUB/CSV/2021-dgz"
date;python3 AIS_Simplificator.py -sd "2021-08-01 00:00:00" -ed "2021-08-31 23:59:59" -pol $Coords -tardir "/mnt/PROJET-CIRMAR/AisData/AISHUB/CSV/2021-dgz"
date;python3 AIS_Simplificator.py -sd "2021-09-01 00:00:00" -ed "2021-09-30 23:59:59" -pol $Coords -tardir "/mnt/PROJET-CIRMAR/AisData/AISHUB/CSV/2021-dgz"
date;python3 AIS_Simplificator.py -sd "2021-10-01 00:00:00" -ed "2021-10-31 23:59:59" -pol $Coords -tardir "/mnt/PROJET-CIRMAR/AisData/AISHUB/CSV/2021-dgz"
date;python3 AIS_Simplificator.py -sd "2021-11-01 00:00:00" -ed "2021-11-30 23:59:59" -pol $Coords -tardir "/mnt/PROJET-CIRMAR/AisData/AISHUB/CSV/2021-dgz"
date;python3 AIS_Simplificator.py -sd "2021-12-01 00:00:00" -ed "2021-12-31 23:59:59" -pol $Coords -tardir "/mnt/PROJET-CIRMAR/AisData/AISHUB/CSV/2021-dgz"
date;ls -l
date;python3 AIS_column_filtered.py
date;ls -l filtered-OH/
date;gzip -v filtered-OH/*.csv
date;ls -l filtered-OH/
date
echo "#############################@"

