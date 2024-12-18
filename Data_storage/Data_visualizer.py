import seaborn as sns
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#TODO list
    #Generar diagrama de puntos para todo tipo de datos,en un franja de tiempo, un mes determinado, lo que va de año
    #Generar un diagrama donde se superpongan x dias o el mes entero

Historical_weather_path="/home/ruiz17/meteo/Data_storage/Storage/Historical_weather.xlsx"
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


def generate_image(args):
    sns.set_theme(style="whitegrid")
    day_1,month_1,year_1=def_data_time(args.fecha_1)
    df=pd.read_excel(Historical_weather_path,sheet_name=year_1)
    if not args.fecha_2:
        df_filter = df[(df['Dia'] == day_1) & (df['Mes'] == month_1)]
        if args.temperatura:
            plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
            sns.lineplot(x="Hora", y="temp (C)", data=df_filter, marker="o", linestyle="-", color="b")
        elif args.precipitacion:
            plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
            sns.lineplot(x="Hora", y="precipitation (mm/h)", data=df_filter, marker="o", linestyle="-", color="b")
        elif args.humedad:
            plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
            sns.lineplot(x="Hora", y="hum(%)", data=df_filter, marker="o", linestyle="-", color="b")
        elif args.presion:
            plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
            sns.lineplot(x="Hora", y="pres(hPa)", data=df_filter, marker="o", linestyle="-", color="b")
        elif args.viento:
            plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
            sns.lineplot(x="Hora", y="wind_speed(m/s)", data=df_filter, marker="o", linestyle="-", color="b")
    else:
        day_2,month_2,year_2=def_data_time(args.fecha_2)
        if year_1==year_2:
            df_filter = df[((df['Dia'] == day_1) & (df['Mes'] == month_1)) |((df['Dia'] == day_2) & (df['Mes'] == month_2))].copy()
            if args.temperatura:
                df_filter['Fecha'] = df_filter['Dia'].astype(str) + '-' + df_filter['Mes']
                # Graficar con Seaborn diferenciando los días por color
                plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
                sns.lineplot(x="Hora", y="temp (C)", data=df_filter, hue="Fecha", marker="o", linestyle="-")
        else:
            df_1=pd.read_excel(Historical_weather_path,sheet_name=year_1)
            df_2=df=pd.read_excel(Historical_weather_path,sheet_name=year_2)
            df_filter = df[((df_1['Dia'] == day_1) & (df_1['Mes'] == month_1)) |((df_2['Dia'] == day_2) & (df_2['Mes'] == month_2))].copy()
            if args.temperatura:
                df_filter['Fecha'] = df_filter['Dia'].astype(str) + '-' + df_filter['Mes']
                # Graficar con Seaborn diferenciando los días por color
                plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
                sns.lineplot(x="Hora", y="temp (C)", data=df_filter, hue="Fecha", marker="o", linestyle="-")


    plt.tight_layout()  # Ajusta el layout para evitar cortes
    plt.xticks(rotation=45)  # Rotar etiquetas 45 grados
    plt.show()




if __name__ == "__main__":
    args=argparser()
    generate_image(args)