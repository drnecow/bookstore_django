from django.contrib import admin
from supply.models import SupplyStatus, Supplier, SupplyEntry, SuppliedBook

# Register your models here.
admin.site.register(SupplyStatus)
admin.site.register(Supplier)
admin.site.register(SupplyEntry)
admin.site.register(SuppliedBook)
