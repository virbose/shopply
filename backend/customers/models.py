from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Customer(AbstractUser):
    contact_number = models.CharField(max_length=12, null=True, blank=True)
    street_1 = models.CharField(max_length=100, null=True, blank=True)
    street_2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'customers'
