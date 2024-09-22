weather_icons = {
    "clear sky": "fas fa-sun",
    "few clouds": "fas fa-cloud-sun",
    "scattered clouds": "fas fa-cloud",
    "broken clouds": "fas fa-cloud-meatball",
    "shower rain": "fas fa-cloud-showers-heavy",
    "rain": "fas fa-cloud-rain",
    "thunderstorm": "fas fa-bolt",
    "snow": "fas fa-snowflake",
    "mist": "fas fa-smog",
    "haze":"fa-solid fa-cloud-sun"
}

import requests
import os
from django.http import JsonResponse
from django.shortcuts import render
from .models import WeatherData
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg

API_KEY = 'b5636a9a80655a31fbcb8b271ac213ae'  
API_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Fetch weather data from the API
def fetch_weather(city):
    response = requests.get(f"{API_URL}?q={city}&units=metric&appid={API_KEY}")
    return response.json()

def check_alerts(weather_data):
    alerts = []
    
    if 'main' in weather_data:
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        dew_point = weather_data.get('dew_point', None)  # Some APIs may not include this directly

        # Temperature alerts
        if temp > 35:
            alerts.append("Extreme heat alert!")
        elif temp < 0:
            alerts.append("Freezing cold alert!")
        
        # Humidity alerts
        if humidity > 80:
            alerts.append("High humidity alert!")
        elif humidity < 20:
            alerts.append("Low humidity alert!")

        # Pressure alerts
        if pressure < 1000:
            alerts.append("Low pressure alert! Possible stormy weather.")
        elif pressure > 1020:
            alerts.append("High pressure alert! Expect clear skies.")

        # Dew Point alerts
        if dew_point and dew_point > 24:
            alerts.append("Uncomfortable humidity levels due to high dew point.")
    
    # Wind speed alert
    if 'wind' in weather_data:
        wind_speed = weather_data['wind']['speed']
        if wind_speed > 10:
            alerts.append("Strong wind alert!")

    # Visibility alert
    if 'visibility' in weather_data:
        visibility_km = weather_data['visibility'] / 1000  # Convert from meters to kilometers
        if visibility_km < 1:
            alerts.append("Low visibility alert! Drive with caution.")

    return alerts


# Store weather data in the database
def fetch_weather_and_store(request, city):
    data = fetch_weather(city)
    if 'main' in data:
        WeatherData.objects.create(
            city=city,
            temperature=data['main']['temp'],
            humidity=data['main']['humidity']
        )
    return JsonResponse({'message': f'Weather data for {city} saved successfully!'})

# Calculate weather trends for the past 24 hours
def get_weather_trends(city):
    last_24_hours = timezone.now() - timedelta(hours=24)
    weather_data = WeatherData.objects.filter(city=city, timestamp__gte=last_24_hours)

    if weather_data.exists():
        avg_temperature = weather_data.aggregate(Avg('temperature'))['temperature__avg']
        avg_humidity = weather_data.aggregate(Avg('humidity'))['humidity__avg']
        return {
            'avg_temperature': avg_temperature,
            'avg_humidity': avg_humidity,
        }
    return None

# Display weather information and alerts
# def weather_view(request):
#     if request.method == "POST":
#         city = request.POST.get('city')
#         weather_data = fetch_weather(city)

#         if 'main' in weather_data:
#             alerts = check_alerts(weather_data)
#             context = {
#                 'temperature': weather_data['main']['temp'],
#                 'humidity': weather_data['main']['humidity'],
#                 'alerts': alerts,
#                 'city': city,
#             }
#             fetch_weather_and_store(request, city)  # Store data in the DB
#             return render(request, 'weather/weather_detail.html', context)
#         else:
#             error_message = weather_data.get('message', 'Failed to fetch weather data')
#             return render(request, 'weather/weather_error.html', {'error_message': error_message})

#     return render(request, 'weather/weather_form.html')

# def weather_view(request):
#     if request.method == "POST":
#         city = request.POST.get('city')
#         weather_data = fetch_weather(city)

#         if 'main' in weather_data:
#             alerts = check_alerts(weather_data)
#             weather_description = weather_data['weather'][0]['description']
#             icon_class = weather_icons.get(weather_description.lower(), 'fas fa-question')  # Default to question mark if no match
#             feels_like = weather_data['main']['feels_like']
#             wind_speed = weather_data['wind']['speed']
#             pressure = weather_data['main']['pressure']
#             humidity = weather_data['main']['humidity']
#             dew_point = round(weather_data['main']['temp'] - ((100 - humidity) / 5))
#             visibility = weather_data['visibility'] / 1000  # km

#             context = {
#                 'temperature': weather_data['main']['temp'],
#                 'feels_like': feels_like,
#                 'wind_speed': wind_speed,
#                 'pressure': pressure,
#                 'humidity': humidity,
#                 'dew_point': dew_point,
#                 'visibility': visibility,
#                 'weather_description': weather_description.capitalize(),
#                 'icon_class': icon_class,
#                 'alerts': alerts,
#                 'city': city,
#             }
#             fetch_weather_and_store(request, city)  # Store data in the DB
#             return render(request, 'weather/weather_detail.html', context)
#         else:
#             error_message = weather_data.get('message', 'Failed to fetch weather data')
#             return render(request, 'weather/weather_error.html', {'error_message': error_message})

#     return render(request, 'weather/weather_form.html')

def weather_view(request):
    trends = None  # Initialize trends variable

    if request.method == "POST":
        city = request.POST.get('city')
        weather_data = fetch_weather(city)

        if 'main' in weather_data:
            alerts = check_alerts(weather_data)
            context = {
                'temperature': weather_data['main']['temp'],
                'feels_like': weather_data['main']['feels_like'],
                'weather_description': weather_data['weather'][0]['description'],
                'icon_class': weather_icons.get(weather_data['weather'][0]['description'], 'fas fa-question'),
                'wind_speed': weather_data['wind']['speed'],
                'pressure': weather_data['main']['pressure'],
                'humidity': weather_data['main']['humidity'],
                'dew_point': round(weather_data['main'].get('dew_point', 0)),
                'visibility': weather_data['visibility'] / 1000,  # Convert meters to kilometers
                'alerts': alerts,
                'city': city,
            }
            fetch_weather_and_store(request, city)  # Store data in the DB
            
            # Fetch weather trends for the city
            trends = get_weather_trends(city)
            context['trends'] = trends
            
            return render(request, 'weather/weather_detail.html', context)
        else:
            error_message = weather_data.get('message', 'Failed to fetch weather data')
            return render(request, 'weather/weather_error.html', {'error_message': error_message})

    return render(request, 'weather/weather_form.html')
