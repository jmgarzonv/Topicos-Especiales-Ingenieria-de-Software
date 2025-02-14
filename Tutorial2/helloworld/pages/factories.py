import factory
from .models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("company")  # Genera un nombre aleatorio
    price = factory.Faker("random_int", min=200, max=9000)  # Precio aleatorio
