from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Customer
# Register your models here.

class CustomerAdmin(DefaultUserAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)
