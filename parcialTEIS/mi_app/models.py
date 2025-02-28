from django.db import models

class Flight(models.Model):
    FLIGHT_TYPES = [
        ('Nacional', 'Nacional'),
        ('Internacional', 'Internacional'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nombre del vuelo")
    flight_type = models.CharField(max_length=15, choices=FLIGHT_TYPES, verbose_name="Tipo de vuelo")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")

    def __str__(self):
        return f"{self.name} - {self.flight_type} - ${self.price}"
