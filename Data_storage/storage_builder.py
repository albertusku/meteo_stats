from datetime import datetime, timezone
import pandas as pd
from Data_storage.stadistics import make_stadistics
import json

timezone_offset=3600
json_config_path="./API/data_api.json"

def unix_to_time(unix_time):
    return datetime.fromtimestamp(unix_time + timezone_offset, tz=timezone.utc)

def create_storage_dataframe(data):
    excel_path="./Data_storage/Storage/Historical_weather.xlsx"
    # data["sunrise"]=unix_to_time(data["sunrise"])
    # data["sunset"]=unix_to_time(data["sunset"])
    now=datetime.now()
    year=now.year
    mes=now.strftime("%B")
    dia=now.day
    hora=now.strftime("%H:%M")
    new_data={"Mes":mes,"Dia":dia,"Hora":hora}
    data={**new_data,**data}
    data.pop("data_time",None)
    print(data) #Para los logs del cron
    df=pd.DataFrame([data])
    df_data=save_excel(df,str(year),excel_path)
    if now.hour == 0 and now.minute == 0: # Implica que un nuevo dia ha empezado
        make_stadistics(df_data)


def save_excel(df,sheet_name,path):
    try:
        with pd.ExcelWriter(path,engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            startrow=writer.sheets[sheet_name].max_row
            df.to_excel(writer, index=False, header=False, sheet_name=sheet_name, startrow=startrow)
    except FileNotFoundError:
        # Si el archivo no existe, crear uno nuevo
        with pd.ExcelWriter(path, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
    print(f"Datos guardados exitosamente en '{path}' en la hoja '{sheet_name}'.")
    return pd.read_excel(path)

def read_json():
    try:
        # Cargar datos desde el archivo JSON
        with open(json_config_path, "r") as file:
            config = json.load(file)

        # Construir los parámetros correctos para la API
        params = {"weather_api":{
            "id": config["weather_api"]["station_id"],       # Nombre de la ciudad
            "appid": config["weather_api"]["api_key"],     # API Key
            "units": config["weather_api"]["units"]  # Unidades (métricas por defecto)
        },
        "tomorrow_api":{"api_key": config["tomorrow_api"]["api_key"],
        "latitude": config["tomorrow_api"]["location"]["latitude"],
        "longitude": config["tomorrow_api"]["location"]["longitude"]}}
        return params

    except FileNotFoundError:
        return "Error: archivo de configuración no encontrado."
    except json.JSONDecodeError:
        return "Error: archivo de configuración JSON inválido."
    
