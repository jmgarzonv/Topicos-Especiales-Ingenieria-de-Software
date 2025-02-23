from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description available")  # Nuevo campo
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )  # Relación con Product
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.product.name}: {self.description[:50]}"
