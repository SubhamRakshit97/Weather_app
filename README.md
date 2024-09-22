# [Weather Analysis System](https://weather-app-1-io9v.onrender.com/) 🌦️

The **Weather Analysis System** is a Django web application that allows users to fetch and display real-time weather data for any city using a public weather API. It provides insights into the current weather conditions and raises alerts for extreme weather events.

## Features 🚀

- Fetch real-time weather data for any city.
- Display weather details like temperature, humidity, wind speed, and weather condition.
- Get alerts for extreme weather conditions like storms, heavy rain, or high wind speeds.
- Easy-to-use interface with city search functionality.
- Responsive design that works across devices.

## Tech Stack 🛠️

- **Backend**: Django 5.1.1
- **Frontend**: HTML5, CSS3, JavaScript
- **API**: OpenWeatherMap API (or any other weather API of your choice)
- **Database**: SQLite (default, can be changed to PostgreSQL or MySQL)
- **Static Files**: Managed using WhiteNoise for production

## Prerequisites ⚙️

- Python 3.x
- Django 5.1.1
- Gunicorn (for deployment)
- API Key from a weather provider (e.g., [OpenWeatherMap](https://openweathermap.org/))

## Getting Started 🏁

To get a local copy of the project up and running, follow these steps.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/weather-analysis-system.git
cd weather-analysis-system
```

### 2. Install Dependencies
Create a virtual environment and install the dependencies listed in the requirements.txt file.

bash
Copy code
# Create a virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate  # On Windows, use `env\Scripts\activate`

# Install dependencies
pip install -r requirements.txt


### 3. Get Your Weather API Key
Sign up for an API key at OpenWeatherMap. Then, add the key to your environment variables or settings.py file.

### 4. Update settings.py
Add your API key in settings.py:
API_KEY = 'your-openweather-api-key-here'

### 5. Apply Migrations
Run the migrations to set up the database.

```bash
python manage.py migrate
```
### 6. Collect Static Files
Run the following command to collect static files:

```bash
python manage.py collectstatic
```

### 7. Run the Application
You can now run the server locally:

```bash
python manage.py runserver
```

### Go to http://localhost:8000 to access the app.
### 8. API endpoint:
Fetch All the details of weather for a particular place: http://127.0.0.1:8000/fetch/

## Deployment 📦
To deploy the Django app on Render, follow these steps:
1. Ensure Gunicorn is installed and configured.
2. Update the start command in Render's dashboard:
```bash
gunicorn weather_analysis.wsgi:application --bind 0.0.0.0:8000
```
3. Set environment variables (such as SECRET_KEY and API_KEY) on Render.
4. Run collectstatic for static file management.

## Configuration for Production 🏭
In your settings.py:
```bash
Set DEBUG = False.
```
Use WhiteNoise to serve static files:
```bash
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```
Add your deployed domain to ALLOWED_HOSTS:
```bash
ALLOWED_HOSTS = ['your-app-name.onrender.com']
```
## Environment Variables 🔐
Ensure the following environment variables are set in your environment:
1. SECRET_KEY: Your Django secret key.
2. API_KEY: The API key for the weather service.
3. DEBUG: Set to False in production.
   
## Screenshots 🖼️
![Screenshot 2024-09-22 162528](https://github.com/user-attachments/assets/3952ab23-1a97-45c9-98ff-044a24d9190a)


![Screenshot 2024-09-22 162607](https://github.com/user-attachments/assets/4a632656-ef86-40a5-9aa8-d07cc0079e60)

## License 📝
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements 🙏
Django Documentation
OpenWeatherMap API
Render Deployment
