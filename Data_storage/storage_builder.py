from datetime import datetime, timezone
import pandas as pd
from Data_storage.Data_handle.stadistics import make_stadistics

timezone_offset=3600


def unix_to_time(unix_time):
    return datetime.fromtimestamp(unix_time + timezone_offset, tz=timezone.utc)

def create_storage_dataframe(data):
    excel_path="/home/ruiz17/meteo/Data_storage/Historical_weather.xlsx"
    # data["sunrise"]=unix_to_time(data["sunrise"])
    # data["sunset"]=unix_to_time(data["sunset"])
    now=datetime.now()
    year=now.year
    mes=now.strftime("%B")
    dia=now.day
    hora=now.strftime("%H:%M:%S")
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
    
