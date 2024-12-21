from API.API_connection import *
from Data_storage.storage_builder import *
from Data_storage.WebApp.app import check_web_up,run_web
import time

# Ejemplo de uso
if __name__ == "__main__":
    params=read_json()
    data = get_current_data(params)
    create_storage_dataframe(data)
    create_BK()
    if not check_web_up():
        run_web()
        time.sleep(5)
    #TODO list
        #crear como una especie de dif entre la raspi y el pc
        #Permitir el el bk de lo que hay en la raspi si el codigo que esta en la raspi funciona
        #Hacer que antes del push_to_raspi se ejecute el programa y si funciona si suba el codigo
        #Poder ejecutar una prueba sin que se guarden los datos
