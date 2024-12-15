import requests
import json

json_config_path="/home/ruiz17/meteo/API/data_api.json"
json_weather_api_output_path="/home/ruiz17/meteo/API/api_weather_response.json"
json_tomorrow_api_output_path="/home/ruiz17/meteo/API/api_tomorrow_response.json"
weather_api_url = "https://api.openweathermap.org/data/2.5/weather"
tomorrow_api_url= url = "https://api.tomorrow.io/v4/weather/forecast"

dict_api={"tomorrow_api":tomorrow_api_url,"weather_api":weather_api_url}
data={}

def get_current_data(params):

    for name,url in dict_api.items():
        response=get_data_from_api(name,url,params[name])
        data.update(response)
    return data

def get_data_from_api(name,url,params):
    try:
        if name=="weather_api":
            response = requests.get(url, params=params)
            response.raise_for_status()  # Lanza una excepción si hay un error HTTP
            # Parsear la respuesta JSON
            data = response.json()
            with open(json_weather_api_output_path, "w") as file:
                    json.dump(data, file, indent=4)  # Formato legible para humanos
            # Extraer datos
            humidity= data["main"]["humidity"]
            pressure=data["main"]["pressure"]
            wind_speed=data["wind"]["speed"]
            # sunrise=data["sys"]["sunrise"]
            #sunset=data["sys"]["sunset"]
            return {"hum(%)":humidity,"pres(hPa)":pressure,"wind_speed(m/s)":wind_speed}
        
        elif name=="tomorrow_api":
            url = f"https://api.tomorrow.io/v4/timelines?location={params['latitude']},{params['longitude']}&fields=precipitationIntensity,temperature&timesteps=30m&units=metric&apikey={params['api_key']}"
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción si hay un error HTTP
            # Parsear la respuesta JSON
            data = response.json()
            with open(json_tomorrow_api_output_path, "w") as file:
                json.dump(data, file, indent=4)
            intervals = data["data"]["timelines"][0]["intervals"]
            # Extraer el primer intervalo (ejemplo de datos actuales)
            first_interval = intervals[0]
            precipitation = first_interval["values"].get("precipitationIntensity", "N/A")
            temperature = first_interval["values"].get("temperature", "N/A")

            # Devolver solo los valores de precipitationIntensity
            return {"temp (C)": temperature,
            "precipitation (mm/h)": precipitation}

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}"
        
def read_json():
    try:
        # Cargar datos desde el archivo JSON
        with open(json_config_path, "r") as file:
            config = json.load(file)

        # Construir los parámetros correctos para la API
        params = {"weather_api":{
            "id": config["weather_api"]["station_id"],       # Nombre de la ciudad
            "appid": config["weather_api"]["api_key"],     # API Key
            "units": config["weather_api"]["units"]  # Unidades (métricas por defecto)
        },
        "tomorrow_api":{"api_key": config["tomorrow_api"]["api_key"],
        "latitude": config["tomorrow_api"]["location"]["latitude"],
        "longitude": config["tomorrow_api"]["location"]["longitude"]}}
        return params

    except FileNotFoundError:
        return "Error: archivo de configuración no encontrado."
    except json.JSONDecodeError:
        return "Error: archivo de configuración JSON inválido."