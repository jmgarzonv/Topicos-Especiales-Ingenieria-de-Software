from django.core.management.base import BaseCommand
from pages.factories import ProductFactory


class Command(BaseCommand):
    help = "Seed the database with products"

    def handle(self, *args, **kwargs):
        ProductFactory.create_batch(8)  # Crea 8 productos aleatorios
        self.stdout.write(self.style.SUCCESS("Successfully seeded products"))
