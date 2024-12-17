import pandas as pd
from datetime import datetime


def make_stadistics(df):
    last_day_data=df.iloc[-2]
    previous_day=last_day_data['Dia']
    previous_month=last_day_data['Mes']
    df_data_day=make_stadistics_day(df,previous_day,previous_month) 
    df_data_month=make_stadistics_month(df_data_day,previous_month)

def make_stadistics_day(df,day,month):
    excel_stadistics_day_path="/home/ruiz17/meteo/Data_storage/Data_handle/Stadistics_day.xlsx"
    now=datetime.now()
    year=now.year
    keys=["temp_max","temp_min","temp_mean","precipitaciones_totales","precipitacion_max_1h","wind_speed_max"]
    temp_max=df[(df['Mes'] == month) & (df['Dia'] == day)]['temp (C)'].max()
    temp_min=df[(df['Mes'] == month) & (df['Dia'] == day)]['temp (C)'].min()
    temp_mean=df[(df['Mes'] == month) & (df['Dia'] == day)]['temp (C)'].mean()
    precipitaciones_totales = df['precipitation (mm/h)'].sum()
    df['Precipitacion_1h'] = df['precipitation (mm/h)'].rolling(window=2).sum()
    precipitacion_max_1h = df['Precipitacion_1h'].max()
    wind_speed_max=df[(df['Mes'] == month) & (df['Dia'] == day)]['wind_speed(m/s)'].max()
    values=[temp_max,temp_min,temp_mean,precipitaciones_totales,precipitacion_max_1h,wind_speed_max]
    data_day=dict(zip(keys,values))
    new_data={"Mes":month,"Dia":day}
    data_day={**new_data,**data_day}
    df_data_day=pd.DataFrame([data_day])
    from Data_storage.storage_builder import save_excel
    return save_excel(df_data_day,str(year),excel_stadistics_day_path)

def make_stadistics_month(df,month):
    #TODO Indicar el dia de las temepraturas maximas y minimas
    excel_stadistics_month_path="/home/ruiz17/meteo/Data_storage/Data_handle/Stadistics_month.xlsx"
    now=datetime.now()
    year=now.year
    keys=["temp_max","temp_min","temp_mean","precipitaciones_totales","wind_speed_max"]
    temp_max=df[(df['Mes']==month)]['temp (C)'].max()
    temp_min=df[(df['Mes']==month)]['temp (C)'].min()
    temp_mean=df[(df['Mes']==month)]['temp (C)'].mean()
    precipitaciones_totales=df[(df['Mes']==month)]['precipitation (mm/h)'].sum()
    wind_speed_max=df[(df['Mes']==month)]['wind_speed(m/s)'].mean()
    values=[temp_max,temp_min,temp_mean,precipitaciones_totales,wind_speed_max]
    data_month=dict(zip(keys,values))
    new_data={"Mes":month}
    data_month={**new_data,**data_month}
    df_data_month=pd.DataFrame([data_month])
    from Data_storage.storage_builder import save_excel
    return save_excel(df_data_month,str(year),excel_stadistics_month_path)


