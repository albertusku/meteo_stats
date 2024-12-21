#!/bin/bash
set -e  # Detener el script si hay un error

REMOTE_USER="ruiz17"
REMOTE_HOST="pi"
REMOTE_DIR="/home/ruiz17/meteo"
LOCAL_BACKUP_DIR="/home/ruiz17/meteo/BK"
LOG_DIR="/home/ruiz17/meteo/Logs_history"
LOG_FILE="${LOG_DIR}/deploy_$(date +'%Y-%m-%d_%H-%M-%S').log"

# Crear la carpeta de logs si no existe
mkdir -p $LOG_DIR

echo "---------INICIANDO PROCESO DE DESPLIEGUE--------" | tee -a $LOG_FILE
echo "$(date): Iniciando despliegue..." | tee -a $LOG_FILE

echo "---------CREANDO BACKUP DE LA RASPI--------" | tee -a $LOG_FILE
TIMESTAMP=$(date +'%Y-%m-%d_%H-%M-%S')
scp -r ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR} ${LOCAL_BACKUP_DIR}/meteo_${TIMESTAMP} | tee -a $LOG_FILE

echo "---------GUARDANDO DATOS IMPORTANTES--------" | tee -a $LOG_FILE
./pull_data_to_PC.sh | tee -a $LOG_FILE

echo "Eliminando archivos .txt locales antiguos..." | tee -a $LOG_FILE
find /home/ruiz17/meteo -type f -name "*.txt" ! -name "requirements.txt" -exec rm -v {} \; | tee -a $LOG_FILE

echo "Creando archivo de marca de tiempo..." | tee -a $LOG_FILE
touch "${LOCAL_BACKUP_DIR}/${TIMESTAMP}.txt" | tee -a $LOG_FILE

echo "---------SUBIENDO DATOS A LA RASPBERRY--------" | tee -a $LOG_FILE
scp -r /home/ruiz17/meteo ${REMOTE_USER}@${REMOTE_HOST}:/home/ruiz17/ | tee -a $LOG_FILE

echo "---------DESPLIEGUE COMPLETADO--------" | tee -a $LOG_FILE
echo "$(date): Despliegue finalizado correctamente." | tee -a $LOG_FILE
