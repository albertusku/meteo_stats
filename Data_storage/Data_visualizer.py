import seaborn as sns
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#TODO list
    #Generar diagrama de puntos para todo tipo de datos,en un franja de tiempo, un mes determinado, lo que va de año

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
    day,month,year=def_data_time(args.fecha_1)
    df=pd.read_excel(Historical_weather_path,sheet_name=year)
    if not args.fecha_2:
        df_filter = df[(df['Dia'] == day) & (df['Mes'] == month)]
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

    plt.tight_layout()  # Ajusta el layout para evitar cortes
    plt.xticks(rotation=45)  # Rotar etiquetas 45 grados
    plt.show()




if __name__ == "__main__":
    args=argparser()
    generate_image(args)