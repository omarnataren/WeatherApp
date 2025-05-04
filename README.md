# Flask Weather App 

Aplicación web simple en **Flask** que consulta el clima actual de una ciudad usando la API de **OpenWeatherMap**

## Estructura del proyecto
- `App.py` — *Código principal de Flask*
- `.env` — *Variables de entorno*
- `/templates` — *Templates HTML para Flask*
- `/static` — *Imágenes y hoja de estilos CSS*


## Cómo correr la aplicación

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/flask-weather-app.git
cd flask-weather-app
```

2. Crea y activa el entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install flask requests python-dotenv
```

4. Configura tu archivo .env
```ini
API_KEY=tu_clave_de_openweathermap
```

5. Corre la aplicación:
```bash
python App.py
```

6. Abre en tu navegador

## Licencia
El proyecto se puede modificar y usar libremente sin fines comerciales