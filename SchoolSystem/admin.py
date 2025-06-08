
from .models import Item, ItemType, ItemStatus, Booking
from django.contrib import admin

admin.site.register(Item)
admin.site.register(ItemType)
admin.site.register(ItemStatus)
admin.site.register(Booking)

