from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os
app = Flask(__name__)

def get_weather(city_name):
    load_dotenv(dotenv_path=".env")
    api_key = os.getenv('API_KEY')

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=es&units=metric&appid={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        weather = {
        'city': data['name'],
        'description': data['weather'][0]['description'],
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity']
        }
        return weather
    else:
        print(f"Error: {response.status_code}")
        return None

get_weather('Oaxaca')


@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    if request.method == 'POST':
        city = request.form.get('city') 
        weather = get_weather(city)

    return render_template('index.html', weather=weather)

if __name__ == '__main__':
    app.run(debug=True)