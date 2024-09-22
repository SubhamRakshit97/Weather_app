# from django.urls import path
# from .views import fetch_weather_and_store, weather_view, weather_trends_view

# urlpatterns = [
#     path('fetch/<str:city>/', fetch_weather_and_store, name='fetch_weather_and_store'),
#     path('weather/<str:city>/', weather_view, name='weather_view'),
#     path('trends/<str:city>/', weather_trends_view, name='weather_trends_view'),
# ]

from django.urls import path
from .views import weather_view

app_name = 'weather'

urlpatterns = [
    path('', weather_view, name='weather'),
]

