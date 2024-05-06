from django.contrib import admin
from core import models

admin.register(models.Product)
admin.register(models.Review)
admin.register(models.Order)
admin.register(models.OrderItem)
admin.register(models.ShippingAddress)
