from API.API_connection import *
from Data_storage.storage_builder import *

# Ejemplo de uso
if __name__ == "__main__":
    params=read_json()
    data = get_current_data(params)
    create_storage_dataframe(data)
    
