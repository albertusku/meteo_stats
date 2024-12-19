import seaborn as sns
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os

#TODO list
    #Generar diagrama de puntos para todo tipo de datos,en un franja de tiempo, un mes determinado, lo que va de año
    #Generar un diagrama donde se superpongan x dias o el mes entero
    #Chekar si hay alguna hora que no es exacta y ponerla exacta

Historical_weather_path="./Storage/Historical_weather.xlsx"
meses = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"]

def argparser():
    parser=argparse.ArgumentParser()
    parser.add_argument("fecha_1", type=str, help="Fecha inicial en formato dd/mm/yyyy")
    parser.add_argument("fecha_2", type=str, nargs="?", help="Fecha final en formato dd/mm/yyyy (opcional)")
    parser.add_argument("-t", "--temperatura", action="store_true", help="Opción para obtener la temperatura")
    parser.add_argument("-p", "--precipitacion", action="store_true", help="Opción para obtener la precipitacion")
    parser.add_argument("-H", "--humedad", action="store_true", help="Opción para obtener la humedad")
    parser.add_argument("-v", "--viento", action="store_true", help="Opción para obtener la viento")
    parser.add_argument("-P", "--presion", action="store_true", help="Opción para obtener la presion")
    args=parser.parse_args()
    return args

def def_data_time(fecha):
    day,month,year=fecha.split("/")
    month=meses[int(month)-1]
    return int(day),month,year

def generate_image(args,df,mod=None):
    key=get_key(args)
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
    sns.lineplot(x="Hora", y=key, data=df, marker="o", linestyle="-", color="b",hue=mod)
    plt.tight_layout()  # Ajusta el layout para evitar cortes
    plt.xticks(rotation=45)  # Rotar etiquetas 45 grados
    plt.show()

def get_key(args):
    if args.temperatura:
        return "temp (C)"
    elif args.precipitacion:
        return "precipitation (mm/h)"
    elif args.humedad:
        return "hum(%)"
    elif args.presion:
        return "pres(hPa)"
    elif args.viento:
        return "wind_speed(m/s)"
    
def handle_images(args):
    day_1,month_1,year_1=def_data_time(args.fecha_1)
    df=pd.read_excel(Historical_weather_path,sheet_name=year_1)
    if not args.fecha_2:
        df_filter = df[(df['Dia'] == day_1) & (df['Mes'] == month_1)]
        generate_image(args,df_filter)
    else:
        day_2,month_2,year_2=def_data_time(args.fecha_2)
        if year_1==year_2:
            df_filter = df[((df['Dia'] == day_1) & (df['Mes'] == month_1)) |((df['Dia'] == day_2) & (df['Mes'] == month_2))].copy()
            df_filter['Fecha'] = df_filter['Dia'].astype(str) + '-' + df_filter['Mes']
            generate_image(args,df_filter,mod='Fecha')      
        else:
            df_1=pd.read_excel(Historical_weather_path,sheet_name=year_1)
            df_2=df=pd.read_excel(Historical_weather_path,sheet_name=year_2)
            df_filter = df[((df_1['Dia'] == day_1) & (df_1['Mes'] == month_1)) |((df_2['Dia'] == day_2) & (df_2['Mes'] == month_2))].copy()
            generate_image(args,df_filter,mod='Fecha')
        
if __name__ == "__main__":
    os.system(".././pull_data_to_PC.sh")
    args=argparser()
    handle_images(args)