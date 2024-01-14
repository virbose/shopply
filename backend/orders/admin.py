from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.


class OrderItemAdmin(admin.ModelAdmin):
    pass

class OrderItemTabAdmin(admin.TabularInline):
    model=OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTabAdmin]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
