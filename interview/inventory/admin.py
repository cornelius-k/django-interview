from django.contrib import admin
from .models import Inventory, InventoryType, InventoryTag, InventoryLanguage

# add inventory models to admin
admin.site.register(Inventory)
admin.site.register(InventoryType)
admin.site.register(InventoryTag)
admin.site.register(InventoryLanguage)
