from django.urls import path
from .views import weather_view,fetch_weather_data

app_name = 'weather'

urlpatterns = [
    path('', weather_view, name='weather'),
    path('fetch/', fetch_weather_data, name='fetch_weather_data')
]
