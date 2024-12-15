import requests
import json

json_config_path="/home/ruiz17/meteo/API/data_api.json"
json_output_path="/home/ruiz17/meteo/API/api_response.json"

def get_current_data(params):
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    # Parámetros de la consulta

    try:
        # Solicitud a la w
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Lanza una excepción si hay un error HTTP

        # Parsear la respuesta JSON
        data = response.json()
        with open(json_output_path, "w") as file:
                json.dump(data, file, indent=4)  # Formato legible para humanos

        # Extraer datos
        temperature = data["main"]["temp"]
        humidity= data["main"]["humidity"]
        pressure=data["main"]["pressure"]
        wind_speed=data["wind"]["speed"]
        # sunrise=data["sys"]["sunrise"]
        #sunset=data["sys"]["sunset"]
        dt=data["dt"]
        return {"temp":temperature,"hum":humidity,"pres":pressure,"wind_speed":wind_speed,"data_time":dt}

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}"
    except KeyError:
        return "Error: no se pudo extraer la temperatura de la respuesta de la API."
    
def read_json():
    try:
        # Cargar datos desde el archivo JSON
        with open(json_config_path, "r") as file:
            config = json.load(file)

        # Construir los parámetros correctos para la API
        params = {
            "id": config["station_id"],       # Nombre de la ciudad
            "appid": config["api_key"],     # API Key
            "units": config.get("units", "metric")  # Unidades (métricas por defecto)
        }
        return params

    except FileNotFoundError:
        return "Error: archivo de configuración no encontrado."
    except json.JSONDecodeError:
        return "Error: archivo de configuración JSON inválido."