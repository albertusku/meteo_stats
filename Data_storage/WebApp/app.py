from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import os
import requests
import subprocess

app = Flask(__name__)

EXCEL_PATH = '/home/ruiz17/meteo/Data_storage/Storage'
FLASK_PORT = 5000

# --- NUEVAS FUNCIONES ---
def check_web_up():
    try:
        respuesta = requests.get(f'http://localhost:{FLASK_PORT}')
        if respuesta.status_code == 200:
            print("La web está activa.")
            return True
    except requests.exceptions.ConnectionError:
        print("La web no está activa.")
        return False

def run_web():
    print("Iniciando Flask...")
    subprocess.Popen(['python3', '/home/ruiz17/meteo/Data_storage/WebApp/app.py'])

# --- FUNCIONES DE FLASK ---
def cargar_datos():
    archivos = [f for f in os.listdir(EXCEL_PATH) if f.endswith('.xlsx')]
    dfs = {'historical': [], 'daily': [], 'monthly': []}

    for archivo in archivos:
        df = pd.read_excel(os.path.join(EXCEL_PATH, archivo))
        
        if set(['Mes', 'Dia', 'Hora', 'temp (C)']).issubset(df.columns):
            dfs['historical'].append(df)
        elif set(['Mes', 'Dia', 'temp_max']).issubset(df.columns):
            dfs['daily'].append(df)
        elif set(['Mes', 'temp_max']).issubset(df.columns) and 'Dia' not in df.columns:
            dfs['monthly'].append(df)
    
    for key in dfs:
        if dfs[key]:
            dfs[key] = pd.concat(dfs[key], ignore_index=True)

    return dfs

@app.route('/')
def index():
    datos = cargar_datos()

    fig_historical = px.line(
        datos['historical'], 
        x='Hora', y='temp (C)', 
        color='Dia', 
        title='Temperatura por Hora (Histórico)'
    ) if not datos['historical'].empty else None

    fig_daily = px.bar(
        datos['daily'], 
        x='Dia', y=['temp_max', 'temp_min'], 
        color='Mes', 
        title='Temperaturas Máxima y Mínima por Día'
    ) if not datos['daily'].empty else None

    fig_monthly = px.line(
        datos['monthly'], 
        x='Mes', y='temp_mean', 
        title='Temperatura Media Mensual'
    ) if not datos['monthly'].empty else None

    return render_template(
        'index.html', 
        grafico_historical=fig_historical.to_html(full_html=False) if fig_historical else '',
        grafico_daily=fig_daily.to_html(full_html=False) if fig_daily else '',
        grafico_monthly=fig_monthly.to_html(full_html=False) if fig_monthly else ''
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=FLASK_PORT)
