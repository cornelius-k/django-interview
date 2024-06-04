from django.contrib import admin
from .models import Order, OrderTag

# add order models to admin
admin.site.register(Order)
admin.site.register(OrderTag)
