import pandas as pd
from datetime import datetime


def make_stadistics(df):
    #TODO list
        #Resumen de lo que va de mes(solo se genera cuando empieza un nuevo dia)
            #Se tiene que guardar en un excel llamado Stadistics_month.xlxs, cada fila sera un mes
            #Temperatura maxima y minima indicando que dias fueron
            #Temperatura media del mes
            #Precipitacion acumulada
            #Precipitacion maxima de un dia
            #Velocidad maxima del viento y que dia fue
    last_day_data=df.iloc[-2]
    previous_day=last_day_data['Dia']
    previous_month=last_day_data['Mes']
    df_data_day=make_stadistics_day(df,previous_day,previous_month) 
    make_stadistics_month(df_data_day)

def make_stadistics_day(df,day,month):
    excel_stadistics_day_path="/home/ruiz17/meteo/Data_storage/Data_handle/Stadistics_day.xlsx"
    now=datetime.now()
    year=now.year
    keys=["temp_max","tem_min","temp_mean","precipitaciones_totales","precipitacion_max_1h","wind_speed_max"]
    temp_max=df[(df['Mes'] == month) & (df['Dia'] == day)]['temp (C)'].max()
    tem_min=df[(df['Mes'] == month) & (df['Dia'] == day)]['temp (C)'].min()
    temp_mean=df[(df['Mes'] == month) & (df['Dia'] == day)]['temp (C)'].mean()
    precipitaciones_totales = df['precipitation (mm/h)'].sum()
    df['Precipitacion_1h'] = df['precipitation (mm/h)'].rolling(window=2).sum()
    precipitacion_max_1h = df['Precipitacion_1h'].max()
    wind_speed_max=df[(df['Mes'] == month) & (df['Dia'] == day)]['wind_speed(m/s)'].max()
    values=[temp_max,tem_min,temp_mean,precipitaciones_totales,precipitacion_max_1h,wind_speed_max]
    data_day=dict(zip(keys,values))
    new_data={"Mes":month,"Dia":day}
    data_day={**new_data,**data_day}
    df_data_day=pd.DataFrame([data_day])
    from Data_storage.storage_builder import save_excel
    return save_excel(df_data_day,str(year),excel_stadistics_day_path)

def make_stadistics_month(df,month):
    excel_stadistics_month_path="/home/ruiz17/meteo/Data_storage/Data_handle/Stadistics_month.xlsx"
    now=datetime.now()
    year=now.year
    keys=["temp_max","tem_min","temp_mean","precipitaciones_totales","wind_speed_max"]
    temp_max=df[(df['Mes']==month)]['temp (C)'].max()
    #Hay que coger el mes actual del df y despues ir sacando toda la data que se necesita
    pass


