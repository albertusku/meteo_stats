#!/bin/bash
set -e  # Detener el script si hay un error

REMOTE_USER="ruiz17"
REMOTE_HOST="pi"
REMOTE_PATH="/home/ruiz17/meteo/Data_storage/Storage/"
LOCAL_PATH="/home/ruiz17/meteo/Data_storage/Storage/"
LOG_DIR="/home/ruiz17/meteo/Logs_history"
LOG_FILE="${LOG_DIR}/pull_data_$(date +'%Y-%m-%d_%H-%M-%S').log"

# Crear la carpeta de logs si no existe
mkdir -p $LOG_DIR

echo "--------- INICIANDO TRANSFERENCIA DE DATOS ---------" | tee -a $LOG_FILE
echo "$(date): Iniciando sincronización de archivos..." | tee -a $LOG_FILE

# Lista de archivos a transferir
FILES=(
  "Historical_weather.xlsx"
  "Stadistics_day.xlsx"
  "Stadistics_month.xlsx"
)

# Transferir cada archivo
for FILE in "${FILES[@]}"; do
  echo "Sincronizando $FILE..." | tee -a $LOG_FILE
  rsync -avz --progress ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}${FILE} ${LOCAL_PATH} | tee -a $LOG_FILE
  
  if [ $? -eq 0 ]; then
    echo "$FILE sincronizado correctamente." | tee -a $LOG_FILE
  else
    echo "Error al sincronizar $FILE" | tee -a $LOG_FILE
  fi
done

echo "$(date): Sincronización completada." | tee -a $LOG_FILE
