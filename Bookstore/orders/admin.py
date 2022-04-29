from django.contrib import admin
from orders.models import OrderStatus, OrderEntry, OrderedBook

# Register your models here.
admin.site.register(OrderStatus)
admin.site.register(OrderEntry)
admin.site.register(OrderedBook)
