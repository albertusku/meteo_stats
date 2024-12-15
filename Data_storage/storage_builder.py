from datetime import datetime, timezone
import pandas as pd
from openpyxl import load_workbook

timezone_offset=3600
excel_path="/home/ruiz17/meteo/Data_storage/Historical_weather.xlsx"

def unix_to_time(unix_time):
    return datetime.fromtimestamp(unix_time + timezone_offset, tz=timezone.utc)

def create_storage_dataframe(data):
    # data["sunrise"]=unix_to_time(data["sunrise"])
    # data["sunset"]=unix_to_time(data["sunset"])
    data["data_time"]=unix_to_time(data["data_time"])
    year=data["data_time"].year
    mes=data["data_time"].strftime("%B")
    dia=data["data_time"].day
    hora=data["data_time"].strftime("%H:%M")
    minuto=data["data_time"].strftime("%M")
    new_data={"Mes":mes,"Dia":dia,"Hora":hora}
    data={**new_data,**data}
    data.pop("data_time",None)
    df=pd.DataFrame([data])
    if min==0 or min==30:
        save_excel(df,str(year))

def save_excel(df,sheet_name):
    try:
        with pd.ExcelWriter(excel_path,engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            startrow=writer.sheets[sheet_name].max_row
            df.to_excel(writer, index=False, header=False, sheet_name=sheet_name, startrow=startrow)
    except FileNotFoundError:
        # Si el archivo no existe, crear uno nuevo
        with pd.ExcelWriter(excel_path, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
    print(f"Datos guardados exitosamente en '{excel_path}' en la hoja '{sheet_name}'.")
    
