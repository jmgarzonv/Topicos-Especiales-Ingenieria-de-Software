from django.urls import path
from .views import home, register_flight, list_flights, flight_stats

urlpatterns = [
    path('', home, name='home'),
    path('registrar/', register_flight, name='register_flight'),
    path('listar/', list_flights, name='list_flights'),
    path('estadisticas/', flight_stats, name='flight_stats'),
]
