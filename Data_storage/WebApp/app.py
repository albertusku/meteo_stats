from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import os
import requests
import subprocess

app = Flask(__name__)

EXCEL_PATH = '/home/ruiz17/meteo/Data_storage/Storage'
FLASK_PORT = 5000

# --- FUNCIONES PARA VERIFICAR Y LANZAR FLASK ---
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


# --- CARGAR DATOS DE TODOS LOS EXCEL ---
def cargar_datos():
    archivos = [f for f in os.listdir(EXCEL_PATH) if f.endswith('.xlsx')]
    dfs = []

    for archivo in archivos:
        df = pd.read_excel(os.path.join(EXCEL_PATH, archivo))
        df['Archivo'] = archivo  # Añadir nombre del archivo para referencia
        dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


# --- RUTA PRINCIPAL ---
@app.route('/', methods=['GET', 'POST'])
def index():
    datos = cargar_datos()

    # Obtener lista de meses y días únicos
    meses_disponibles = datos['Mes'].unique() if 'Mes' in datos.columns else []
    dias_disponibles = []

    mes_seleccionado = request.form.get('mes') if request.method == 'POST' else None
    dia_seleccionado = request.form.get('dia') if request.method == 'POST' else None

    # Filtrar días disponibles en función del mes seleccionado
    if mes_seleccionado:
        dias_disponibles = list(datos[datos['Mes'] == mes_seleccionado]['Dia'].dropna().astype(int).unique())


    
    # Filtrar por mes y día (si se seleccionaron ambos)
    if mes_seleccionado and dia_seleccionado:
        dia_seleccionado = int(dia_seleccionado)
        datos = datos[(datos['Mes'] == mes_seleccionado) & (datos['Dia'] == dia_seleccionado)]

    # Generar gráfica (o mensaje si no hay datos)
    if not datos.empty:
        fig = px.line(
            datos, 
            x='Hora', 
            y='temp (C)', 
            title=f'Datos de {dia_seleccionado}/{mes_seleccionado}' if dia_seleccionado else 'Histórico'
        )
        grafico = fig.to_html(full_html=False)
    else:
        grafico = "<p>No hay datos disponibles para esta fecha.</p>"

    return render_template(
        'index.html', 
        grafico=grafico,
        meses_disponibles=meses_disponibles,
        dias_disponibles=dias_disponibles,
        mes_seleccionado=mes_seleccionado,
        dia_seleccionado=dia_seleccionado
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=FLASK_PORT)
