from django.urls import path
from . import views

urlpatterns = [
    path("", views.everest_weather_clean, name="everest_weather_clean"),
    path("api/", views.weather_api, name="weather_api"),
]
