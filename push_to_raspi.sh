scp -r ruiz17@pi:/home/ruiz17/meteo /home/ruiz17/meteo/BK #backup de todo el codigo
./pull_data_to_PC.sh # Guardar datos antes de subir todo el codigo
rm *.txt #Para borrar todos los txt donde estoy
fecha=$(date)
touch "${fecha}.txt" #Para poder idenfiticar el momento del push
scp -r /home/ruiz17/meteo ruiz17@pi:/home/ruiz17/

