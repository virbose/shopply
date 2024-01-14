from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=0)

    @property
    def in_stock(self):
        return self.quantity_in_stock > 0