from API.API_connection import *
from Data_storage.storage_builder import *

# Ejemplo de uso
if __name__ == "__main__":
    params=read_json()
    data = get_current_data(params)
    create_storage_dataframe(data)
    create_BK()
    #TODO list
        #crear como una especie de dif entre la raspi y el pc
        #Permitir el el bk de lo que hay en la raspi si el codigo que esta en la raspi funciona
        #Hacer que todos los paths sean genericos aka que sirva para todo el mundo
        #Hacer que antes del push_to_raspi se ejecute el programa y si funciona si suba el codigo
        #Poder ejecutar una prueba sin que se guarden los datos
