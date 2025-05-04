from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os
import time
from functools import lru_cache

app = Flask(__name__) # Inicializa la app Flask
load_dotenv(dotenv_path=".env") # Carga las varables del .env
session = requests.Session() #Crea una sesión de requests

#Funcion interna cacheada que hace el request
@lru_cache(maxsize=64)
def get_weather(city_name: str):
    city_name = city_name.strip().lower()
    start = time.time()  # Marca el inicio para medir tiempo de respuesta
    api_key = os.getenv('API_KEY') #Obtiene API KEY
    
    url = (f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}")
    
    try:
        # Hace solicitud a la API con timeout 5s
        response = session.get(url, timeout=5)
    except requests.RequestException as e:
        print(f"[Error conexión] {e}")
        return None # SI falla retorna None

    elapsed = time.time() - start #Calcula tiempo de la solicitud y lo imrpime 
    print(f"[_fetch_weather] {city_name}: {elapsed:.2f}s")

    if response.status_code == 200:
        data = response.json() # Decodifica la respuesta JSON
        icono = data['weather'][0]['icon']
        img_url = f'https://openweathermap.org/img/wn/{icono}@2x.png'
        
        #Construcción de diccionario con los datos
        return {
            'city': data['name'],
            'description': data['weather'][0]['description'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'img': img_url,
            'feels_like': data['main']['feels_like'],
            'country': data['sys']['country'],
            'wind_speed': data['wind']['speed'],
            'pressure': data['main']['pressure'],
            'clouds' : data['clouds']['all'],
            'min': data['main']['temp_min'],
            'max': data['main']['temp_max']
        }
    else:
        print(f"[API error] Código: {response.status_code}")
        return None

#Fubnión para cambiar fondo con base a la temperatura
def set_body_bg(temperatura: float) -> str:
    if temperatura <=10:
        return 'frio'
    elif temperatura<=20:
        return 'fresco'
    elif temperatura<=30:
        return 'soleado'
    elif temperatura<=40:
        return 'caluroso'
    else:
        return 'muy-caliente'

@app.route('/', methods=['GET', 'POST'])
def home():
     #Se inicializan variables
    weather = None
    tema = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city', '').strip()  #Obtiene la ciudad del formulario
        if not city:
            error = "Por favor, ingresa el nombre de una ciudad."
        else:
            weather = get_weather(city) #Busa clima
            if weather:
                tema = set_body_bg(weather['temperature']) #Asigna el fondo
            else:
                error = f"No se encontró la ciudad '{city}'. Intenta con otro nombre"
     # Renderiza el template HTML con los datos
    return render_template('index.html', weather=weather, tema=tema, error=error)
#Arranaca el srvidor FLask  en modo debug
if __name__ == '__main__':
    app.run(debug=True)
