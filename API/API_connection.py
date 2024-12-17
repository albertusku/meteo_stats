import requests
import json


json_weather_api_output_path="/home/ruiz17/meteo/API/api_weather_response.json"
json_tomorrow_api_output_path="/home/ruiz17/meteo/API/api_tomorrow_response.json"
weather_api_url = "https://api.openweathermap.org/data/2.5/weather"
tomorrow_api_url= url = "https://api.tomorrow.io/v4/weather/forecast"

dict_api={"tomorrow_api":tomorrow_api_url,"weather_api":weather_api_url}
data={}

def get_current_data(params):
    #TODO list
        #Obtener predicciones para el dia actual,para mañana y para dentro de 3 dias
        #Forma de almacenarlo en un excel llamado /Data_storage/Data_forecast/forecast_predictions.xlxs
            #Primera columana con el dia actual, 3 primeras columnas relacionadas con el dia actual, 3 siguientes con la de mañana y 3 siguientes
            #con lo dentro de 3 dias
            #3 columanas para cada dias porque: temperatura max,min y precipitacion total
        #Controlar excepciones de fallo de api para que lo vuelva a intentar un numero de veces determinado
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
        
